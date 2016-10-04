## no longer needed...
#
# BASE_VALUES = {
#         'betamethason': 0.75,
#         'cortison': 25.0,
#         'dexamethason': 0.75,
#         'hydrocortison': 20.0,
#         'metylprednisolon': 4.0,
#         'prednisolon': 5.0,
#         'prednison': 5.0,
#         'triamcinolon': 4.0,
#     }
#
# ## poradi
# #         'metylprednisolon': 4.0,
# #         'hydrocortison': 20.0,
# #         'dexamethason': 0.75,
# #         'prednison': 5.0,
# #         'prednisolon': 5.0,
# #         'cortison': 25.0,
# #         'betamethason': 0.75,
# #         'triamcinolon': 4.0,
#
# def calculate_values(data):
#     '''calculate correct values based on input data'''
#     if not data:
#         return BASE_VALUES
#
#     # forms supply "None" elsewhere, get rid of it
#     xdata = {}
#     for k, v in data.items():
#         if v is not None:
#             xdata[k] = v
#     data = xdata
#     if len(data) > 1:
#         raise ValueError('Too much data')
#
#     k, v = data.items()[0]
#     base_v = BASE_VALUES[k]
#     factor = float(v) / base_v
#     res = {}
#     for base_k, base_v in BASE_VALUES.items():
#          res[base_k] = base_v * factor
#     return res
