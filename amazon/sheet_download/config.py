# config info

# templates part
templates = {
    'template_1':{
        # including the relation of fields and column names in sheet
        'selected_field': [
            ('orders.AmazonOrderId', 'order ID', ),
            ('orderitems.SellerSKU', 'sku', ),
            ('orderitems.ASIN', 'ASIN', ),
            ('orders.Seller', 'stores', ),
            ('orders.SalesChannel', 'sales channel', ),
            ('inventory.InStockSupplyQuantity', 'stock', ),
            ('orderitems.QuantityOrdered', 'quantity ordered', ),
            ('orders.NumberOfItemsShipped', 'item shipped', ),
            ('orders.NumberOfItemsUnshipped', 'item unshipped', ),
            ('orderitems.ItemPrice_Amount', 'price', ),
            ('orderitems.ItemTax_Amount', 'tax', ),
            ('orderitems.ShippingPrice_Amount', 'ShippingPrice', ),
            ('orderitems.ShippingTax_Amount', 'ShippingTax', ),
            ('orders.Amount', 'amount', ),
            ('orders.CurrencyCode', 'currency', ),
            ('orders.OrderType', 'order type', ),
            ('orders.OrderStatus', 'order status', ),
            ('orders.PurchaseDate', 'purchase date', ),
            ('orders.PaidDate', 'paid date', ),
            ('orders.BuyerName', 'buyer name', ),
            ('orders.Phone', 'buyer phone', ),
            ('orders.CountryCode', 'buyer country', ),
            ('orders.StateOrRegion', 'buyer states or region', ),
            ('orders.City', 'buyer city', ),
            ('orders.PostalCode', 'buyer postal code', ),
            ('orders.AddressLine1', 'buyer adress line1', ),
            ('orders.AddressLine2', 'buyer adress line2', ),
            ('orders.FulfillmentChannel', 'fulfillment channel', ),
        ],
        'conditions': '',
    },

    'template_2':{
        # including the relation of fields and column names in sheet
        'selected_field':[
            ('inventory.SellerSKU', 'sku', ),
            ('inventory.Seller', 'stores', ),
            ('inventory.ASIN', 'ASIN', ),
            ('inventory.FNSKU', 'FNSKU', ),
            ('inventory.InStockSupplyQuantity', 'Stock', ),
            ('price.LandedPrice_Amount', 'Price', ),
            ('price.LandedPrice_CurrencyCode', 'CurrencyCode', ),
        ],
        'conditions': '',
    },
}
