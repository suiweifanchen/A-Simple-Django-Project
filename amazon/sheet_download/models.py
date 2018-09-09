from django.db import models


class Orders(models.Model):
    """
    orers表，保存订单信息
    """
    AmazonOrderId = models.CharField(max_length=50)
    LastUpdateDate = models.DateTimeField()
    PurchaseDate = models.DateTimeField(null=True, default=None)
    PaidDate = models.DateTimeField(null=True, default=None)
    Seller = models.CharField(null=True, max_length=100)
    Amount = models.FloatField(null=True, max_length=10)
    CurrencyCode = models.CharField(null=True, max_length=10)
    OrderType = models.CharField(null=True, max_length=50)
    OrderStatus = models.CharField(null=True, max_length=50)
    SalesChannel = models.CharField(null=True, max_length=100)
    NumberOfItemsShipped = models.IntegerField(null=True)
    NumberOfItemsUnshipped = models.IntegerField(null=True)
    BuyerEmail = models.CharField(null=True, max_length=100)
    BuyerName = models.CharField(null=True, max_length=100)
    Name = models.CharField(null=True, max_length=100)
    Phone = models.CharField(null=True, max_length=50)
    CountryCode = models.CharField(null=True, max_length=50)
    StateOrRegion = models.CharField(null=True, max_length=100)
    City = models.CharField(null=True, max_length=100)
    PostalCode = models.CharField(null=True, max_length=50)
    AddressLine1 = models.CharField(null=True, max_length=500)
    AddressLine2 = models.CharField(null=True, max_length=500)
    AddressType = models.CharField(null=True, max_length=50)
    EarliestShipDate = models.DateTimeField(null=True, default=None)
    LatestShipDate = models.DateTimeField(null=True, default=None)
    EarliestDeliveryDate = models.DateTimeField(null=True, default=None)
    LatestDeliveryDate = models.DateTimeField(null=True, default=None)
    ShipServiceLevel = models.CharField(null=True, max_length=100)
    ShipmentServiceLevelCategory = models.CharField(null=True, max_length=100)
    ShippedByAmazonTFM = models.CharField(null=True, max_length=100)
    MarketplaceId = models.CharField(null=True, max_length=50)
    IsPrime = models.CharField(null=True, max_length=100)
    IsPremiumOrder = models.CharField(null=True, max_length=100)
    IsBusinessOrder = models.CharField(null=True, max_length=100)
    IsReplacementOrder = models.CharField(null=True, max_length=100)
    PaymentMethod = models.CharField(null=True, max_length=100)
    PaymentMethodDetail = models.CharField(null=True, max_length=100)
    FulfillmentChannel = models.CharField(null=True, max_length=100)
    SellerOrderId = models.CharField(null=True, max_length=100)
    RequestId = models.CharField(null=True, max_length=100)

    class Meta:
        db_table = 'orders'
        unique_together = (('AmazonOrderId', 'LastUpdateDate'), )

    def __str__(self):
        return self.AmazonOrderId+ "___" + str(self.LastUpdateDate)


class OrderItems(models.Model):
    """
    orderitems表，保存每个订单所卖产品的具体信息
    """
    AmazonOrderId = models.CharField(max_length=50)
    SellerSKU = models.CharField(max_length=50)
    ASIN = models.CharField(null=True, max_length=50)
    OrderItemId = models.CharField(null=True, max_length=50)
    QuantityOrdered = models.IntegerField(null=True)
    QuantityShipped = models.IntegerField(null=True)
    ConditionId = models.CharField(null=True, max_length=10)
    IsGift = models.CharField(null=True, max_length=10)
    ItemPrice_Amount = models.FloatField(null=True)
    ItemPrice_CurrencyCode = models.CharField(null=True, max_length=10)
    ItemTax_Amount = models.FloatField(null=True)
    ItemTax_CurrencyCode = models.CharField(null=True, max_length=10)
    RequestId = models.CharField(null=True, max_length=50)

    class Meta:
        db_table = 'orderitems'
        unique_together = (('AmazonOrderId', 'SellerSKU'), )

    def __str__(self):
        return self.AmazonOrderId+ "___" + self.SellerSKU


class Inventory(models.Model):
    """
    inventory表，保存SKU的库存信息
    """
    SellerSKU = models.CharField(max_length=50)
    Seller = models.CharField(max_length=50)
    MarketplaceId = models.CharField(max_length=50)
    ASIN = models.CharField(null=True, max_length=50)
    FNSKU = models.CharField(null=True, max_length=50)
    InStockSupplyQuantity = models.IntegerField(null=True)
    Condition = models.CharField(null=True, max_length=50)
    RequestId = models.CharField(null=True, max_length=50)

    class Meta:
        db_table = 'inventory'
        unique_together = (('SellerSKU', 'Seller', 'MarketplaceId'), )

        def __str__(self):
            return self.SellerSKU


class sku(models.Model):
    """
    sku表，保存店铺商品sku
    """
    sku = models.CharField(max_length=50)
    Seller = models.CharField(max_length=50)
    MarketplaceId = models.CharField(max_length=50)
    asin = models.CharField(null=True, max_length=50)
    price = models.FloatField(null=True)
    BusinessPrice = models.FloatField(null=True)
    quantity = models.IntegerField(null=True)
    ReportId = models.CharField(null=True, max_length=50)

    class Meta:
        db_table = 'sku'
        unique_together = (('sku', 'Seller', 'MarketplaceId'), )

        def __str__(self):
            return self.sku


class price(models.Model):
    """
    price表，保存每个sku的价格信息
    """
    SellerSKU = models.CharField(max_length=50)
    SellerId = models.CharField(max_length=50)
    MarketplaceId = models.CharField(max_length=50)
    Seller = models.CharField(null=True, max_length=50)
    ASIN = models.CharField(null=True, max_length=50)
    LandedPrice_Amount = models.FloatField(null=True)
    LandedPrice_CurrencyCode = models.CharField(null=True, max_length=10)
    ListingPrice_Amount = models.FloatField(null=True)
    ListingPrice_CurrencyCode = models.CharField(null=True, max_length=10)
    Shipping_Amount = models.FloatField(null=True)
    Shipping_CurrencyCode = models.CharField(null=True, max_length=10)
    RegularPrice_Amount = models.FloatField(null=True)
    RegularPrice_CurrencyCode = models.CharField(null=True, max_length=10)
    FulfillmentChannel = models.CharField(null=True, max_length=50)
    ItemCondition = models.CharField(null=True, max_length=10)
    ItemSubCondition = models.CharField(null=True, max_length=10)
    RequestId = models.CharField(null=True, max_length=50)

    class Meta:
        db_table = 'price'
        unique_together = (('SellerSKU', 'SellerId', 'MarketplaceId'), )

        def __str__(self):
            self.SellerSKU
