# generated by bezik: 2025_01_22 18:55:38.050078
# github: https://github.com/bezumnui/pyCUDLibcal

class BookingComplete:
	def __init__(__self__, bookId=None, html=None, bookingCost=None, **kwargs):
		__self__._kwargs = kwargs
		__self__.bookId: str = bookId
		__self__.html: str = html
		__self__.bookingCost: int = bookingCost

	def get_cancellation_link(__self__):
		return f"https://cud.libcal.com/equipment/cancel?id={__self__.bookId}"

	def __repr__(__self__):
		return f'BookingComplete[bookId: {__self__.bookId}, html: {__self__.html}, bookingCost: {__self__.bookingCost}]'
