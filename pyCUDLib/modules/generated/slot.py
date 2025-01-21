# generated by bezik: 2025_01_21 19:18:43.868135
# github: https://github.com/bezumnui/pyCUDLibcal

class Slot:
	def __init__(__self__, start=None, end=None, itemId=None, checksum=None, **kwargs):
		__self__._kwargs = kwargs
		__self__.start: str = start
		__self__.end: str = end
		__self__.itemId: int = itemId
		__self__.checksum: str = checksum

	def __repr__(__self__):
		return f'Slot[start: {__self__.start}, end: {__self__.end}, itemId: {__self__.itemId}, checksum: {__self__.checksum}]'
