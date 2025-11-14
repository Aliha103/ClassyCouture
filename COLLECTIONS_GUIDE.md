# Creating Collections with Sub-Collections in ClassyCouture

## Overview
This guide shows you how to create a collection (e.g., "XYZ Collection") with sub-collections (e.g., "Men's XYZ", "Women's XYZ", "Accessories XYZ").

---

## Method 1: Using Enhanced Category Model (Recommended)

### Step 1: Update the Category Model

Add a `parent` field to create hierarchical categories:

```python
# backend/api/models.py

class Category(models.Model):
    """Product category model with hierarchical support."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image_url = models.URLField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        null=True,
        blank=True
    )
    is_collection = models.BooleanField(default=False)  # Mark top-level collections
    display_order = models.IntegerField(default=0)  # For custom ordering
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['display_order', 'name']
        unique_together = [['parent', 'name']]

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    def get_all_children(self):
        """Get all descendant categories."""
        children = list(self.subcategories.all())
        for child in list(children):
            children.extend(child.get_all_children())
        return children
```

### Step 2: Create Database Migration

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Your XYZ Collection via Django Admin

**Option A: Using Django Shell**
```bash
python manage.py shell
```

```python
from api.models import Category

# Create the XYZ Collection (parent)
xyz_collection = Category.objects.create(
    name="XYZ Collection",
    slug="xyz-collection",
    description="Exclusive XYZ Collection featuring premium designs",
    image_url="https://example.com/xyz-collection.jpg",
    is_collection=True,
    display_order=1
)

# Create Sub-Collections
mens_xyz = Category.objects.create(
    name="Men's XYZ",
    slug="mens-xyz",
    description="Men's line from XYZ Collection",
    image_url="https://example.com/mens-xyz.jpg",
    parent=xyz_collection,
    display_order=1
)

womens_xyz = Category.objects.create(
    name="Women's XYZ",
    slug="womens-xyz",
    description="Women's line from XYZ Collection",
    image_url="https://example.com/womens-xyz.jpg",
    parent=xyz_collection,
    display_order=2
)

accessories_xyz = Category.objects.create(
    name="XYZ Accessories",
    slug="xyz-accessories",
    description="Accessories from XYZ Collection",
    image_url="https://example.com/xyz-accessories.jpg",
    parent=xyz_collection,
    display_order=3
)
```

**Option B: Using Django Admin Panel**
1. Go to `http://localhost:8000/admin/`
2. Click on "Categories"
3. Click "Add Category"
4. Fill in the details:
   - Name: "XYZ Collection"
   - Slug: "xyz-collection"
   - Is collection: ✓ (checked)
   - Parent: (leave blank for top-level)
5. Save

Then create sub-collections with "XYZ Collection" as parent.

### Step 4: Update the Serializer

```python
# backend/api/serializers.py

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    subcategories = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'image_url',
            'parent', 'parent_name', 'is_collection', 'display_order',
            'subcategories', 'product_count', 'created_at', 'updated_at'
        ]

    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return CategorySerializer(obj.subcategories.all(), many=True).data
        return []

    def get_product_count(self, obj):
        return obj.products.count()
```

### Step 5: Update the ViewSet

```python
# backend/api/views.py

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Category model."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()

        # Filter for collections only (top-level)
        collections_only = self.request.query_params.get('collections_only')
        if collections_only and collections_only.lower() == 'true':
            queryset = queryset.filter(parent__isnull=True, is_collection=True)

        # Filter for sub-collections of a specific parent
        parent_id = self.request.query_params.get('parent')
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)

        # Get all categories with their subcategories
        return queryset.prefetch_related('subcategories', 'products')
```

### Step 6: Frontend Usage

**Fetch Collections:**
```typescript
// Fetch all collections (top-level)
const response = await fetch('http://localhost:8000/api/categories/?collections_only=true');
const collections = await response.json();

// Fetch sub-collections of XYZ
const xyzId = collections.find(c => c.slug === 'xyz-collection').id;
const subCollections = await fetch(`http://localhost:8000/api/categories/?parent=${xyzId}`);
const xyzSubCollections = await subCollections.json();
```

**Display Collections on Frontend:**
```tsx
// components/CollectionGrid.tsx
export function CollectionGrid() {
  const [collections, setCollections] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/categories/?collections_only=true')
      .then(res => res.json())
      .then(data => setCollections(data));
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {collections.map(collection => (
        <CollectionCard key={collection.id} collection={collection} />
      ))}
    </div>
  );
}
```

---

## Method 2: Using Tags/Labels (Alternative)

If you want to keep categories simple and use tags instead:

### Step 1: Create a Tag Model

```python
# backend/api/models.py

class Tag(models.Model):
    """Tag model for collections and themes."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    tag_type = models.CharField(
        max_length=20,
        choices=[
            ('collection', 'Collection'),
            ('season', 'Season'),
            ('style', 'Style'),
            ('occasion', 'Occasion'),
        ],
        default='collection'
    )

    def __str__(self):
        return self.name

# Update Product model
class Product(models.Model):
    # ... existing fields ...
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)
```

### Step 2: Create XYZ Collection Tags

```python
from api.models import Tag, Product

# Create collection tags
xyz_main = Tag.objects.create(
    name="XYZ Collection",
    slug="xyz-collection",
    tag_type="collection"
)

xyz_mens = Tag.objects.create(
    name="XYZ Men's",
    slug="xyz-mens",
    tag_type="collection"
)

xyz_womens = Tag.objects.create(
    name="XYZ Women's",
    slug="xyz-womens",
    tag_type="collection"
)

# Add tags to products
product = Product.objects.get(id=1)
product.tags.add(xyz_main, xyz_mens)
product.save()
```

---

## Complete Example: Creating "Summer XYZ 2025" Collection

```python
# In Django shell or admin

# 1. Create main collection
summer_xyz = Category.objects.create(
    name="Summer XYZ 2025",
    slug="summer-xyz-2025",
    description="Limited edition summer collection",
    image_url="https://example.com/summer-xyz-2025.jpg",
    is_collection=True,
    display_order=1
)

# 2. Create sub-collections
beach_wear = Category.objects.create(
    name="Beach Wear",
    slug="beach-wear",
    parent=summer_xyz,
    image_url="https://example.com/beach-wear.jpg",
    display_order=1
)

casual_summer = Category.objects.create(
    name="Casual Summer",
    slug="casual-summer",
    parent=summer_xyz,
    image_url="https://example.com/casual-summer.jpg",
    display_order=2
)

summer_accessories = Category.objects.create(
    name="Summer Accessories",
    slug="summer-accessories",
    parent=summer_xyz,
    image_url="https://example.com/summer-accessories.jpg",
    display_order=3
)

# 3. Add products to sub-collections
from api.models import Product

product1 = Product.objects.create(
    name="Floral Beach Dress",
    category=beach_wear,
    price=89.99,
    image_url="https://example.com/beach-dress.jpg",
    inventory=50,
    new_arrival=True
)

product2 = Product.objects.create(
    name="Linen Summer Shirt",
    category=casual_summer,
    price=49.99,
    image_url="https://example.com/linen-shirt.jpg",
    inventory=100,
    featured=True
)
```

---

## API Endpoints After Implementation

```
GET /api/categories/                     # All categories
GET /api/categories/?collections_only=true   # Only top-level collections
GET /api/categories/?parent=5            # Sub-collections of category 5
GET /api/categories/5/                   # Specific collection with subcategories
GET /api/products/?category=5            # Products in specific category
GET /api/products/?collection=xyz-collection  # Products in collection (including sub-collections)
```

---

## Frontend Navigation Structure

```
Home
├── Collections
│   ├── XYZ Collection
│   │   ├── Men's XYZ
│   │   ├── Women's XYZ
│   │   └── Accessories XYZ
│   ├── Summer 2025
│   │   ├── Beach Wear
│   │   ├── Casual Summer
│   │   └── Summer Accessories
│   └── Winter Essentials
│       ├── Coats & Jackets
│       ├── Sweaters
│       └── Winter Accessories
```

---

## Quick Reference Commands

```bash
# Create migration after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Open Django shell
python manage.py shell

# Create superuser for admin access
python manage.py createsuperuser
```

---

## Best Practices

1. **Use Slugs**: Always create URL-friendly slugs for SEO
2. **Images**: Use high-quality images for collections
3. **Descriptions**: Write compelling descriptions for each collection
4. **Display Order**: Use `display_order` to control how collections appear
5. **Validation**: Prevent circular parent relationships
6. **Caching**: Cache collection data for better performance

---

## Need Help?

- Check Django Admin: `http://localhost:8000/admin/`
- API Documentation: `http://localhost:8000/api/`
- View Categories: `http://localhost:8000/api/categories/`
