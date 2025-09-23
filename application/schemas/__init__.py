from application.schemas.user import (
    CreateUser,
    ResponseUser,
    UpdateUser,
    LoginUser,
    ResponseUserWithOrder,
)
from application.schemas.product import (
    CreateProduct,
    ResponseProduct,
    UpdateProduct,
    ResponseProductWithItems,
)
from application.schemas.order import (
    OrderStatus,
    CreateOrder,
    ResponseOrder,
    UpdateOrder,
    ResponseOrderWithRelationship,
)
from application.schemas.order_items import (
    CreateOrderItem,
    ResponseOrderItem,
    UpdateOrderItem,
    ResponseOrderItemWithOutID,
    ResponseOrderItemWithOutProductID,
    ResponseOrderItemAndProduct,
)
from application.schemas.token import TokenResponse

ResponseOrderWithRelationship.model_rebuild()
ResponseUserWithOrder.model_rebuild()
ResponseProductWithItems.model_rebuild()
ResponseOrderItemAndProduct.model_rebuild()
