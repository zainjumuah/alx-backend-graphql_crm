import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from crm.models import Customer, Product, Order
from crm.filters import CustomerFilter, ProductFilter, OrderFilter
from django.core.exceptions import ValidationError
from crm.models import Product  

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node,)
        fields = "__all__"


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)
        fields = "__all__"


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node,)
        fields = "__all__"


# ---------------------------
# QUERIES
# ---------------------------
class Query(graphene.ObjectType):
    customer = graphene.relay.Node.Field(CustomerType)
    all_customers = DjangoFilterConnectionField(CustomerType)

    product = graphene.relay.Node.Field(ProductType)
    all_products = DjangoFilterConnectionField(ProductType)

    order = graphene.relay.Node.Field(OrderType)
    all_orders = DjangoFilterConnectionField(OrderType)


# ---------------------------
# MUTATIONS
# ---------------------------
class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        restock_amount = graphene.Int(default_value=10)

    updated_products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info, restock_amount):
        products = Product.objects.filter(stock__lt=10)
        updated_list = []
        for product in products:
            product.stock += restock_amount
            product.save()
            updated_list.append(product)

        return UpdateLowStockProducts(
            updated_products=updated_list,
            message=f"{len(updated_list)} products restocked successfully"
        )


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()  

# ---------------------------
# ROOT SCHEMA
# ---------------------------
schema = graphene.Schema(query=Query, mutation=Mutation)

