# Views Package
# แยก View ออกเป็นโมดูลอิสระ (แต่ละ View แยกไฟล์อิสระ ไม่รวมกัน)

from .login_view import LoginView
from .rumour_list_view import RumourListView
from .rumour_detail_view import RumourDetailView
from .summary_view import SummaryView

__all__ = ['LoginView', 'RumourListView', 'RumourDetailView', 'SummaryView']
