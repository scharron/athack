import ctypes
import builtins
from smtplib import SMTP
from email.mime.text import MIMEText


# Stolen from forbiddenfruit
# Not sure if really useful
Py_ssize_t = (hasattr(ctypes.pythonapi, 'Py_InitModule4_64') and
              ctypes.c_int64 or ctypes.c_int)


AtBinOp = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object)
IdxOp = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object)


class PyAsNumber(ctypes.Structure):
    pass


PyAsNumber._fields_ = (
    [
        (name, ctypes.c_void_p)
        for name in ['nb_add', 'nb_subtract', 'nb_multiply', 'nb_remainder', 'nb_divmod',
                     'nb_power', 'nb_negative', 'nb_positive', 'nb_absolute',
                     'nb_bool', 'nb_invert', 'nb_lshift', 'nb_rshift', 'nb_and', 'nb_xor', 'nb_or', 'nb_int',
                     'nb_reserved', 'nb_float', 'nb_inplace_add', 'nb_inplace_subtract', 'nb_inplace_multiply', 'nb_inplace_remainder', 'nb_inplace_power',
                     'nb_inplace_lshift', 'nb_inplace_rshift', 'nb_inplace_and', 'nb_inplace_xor', 'nb_inplace_or', 'nb_floor_divide', 'nb_true_divide',
                     'nb_inplace_floor_divide', 'nb_inplace_true_divide',
                     ]
    ] +
    [
        ('nb_index', IdxOp),
        ('nb_matrix_multiply', AtBinOp),
        ('nb_inplace_matrix_multiply', ctypes.c_void_p)
    ]
)


class PyUnicodeType(ctypes.Structure):
    pass


PyUnicodeType._fields_ = [
    ('ob_refcnt', Py_ssize_t),
    ('ob_type', ctypes.POINTER(PyUnicodeType)),
    ('ob_size', Py_ssize_t),
    ('tp_name', ctypes.c_char_p),
    ('tp_basicsize', ctypes.c_int64),
    ('tp_itemsize', ctypes.c_int64),
    ('tp_dealloc', ctypes.c_void_p),
    ('tp_print', ctypes.c_void_p),
    ('tp_getattr', ctypes.c_void_p),
    ('tp_setattr', ctypes.c_void_p),
    ('tp_as_async', ctypes.c_void_p),
    ('tp_repr', ctypes.c_void_p),
    ('tp_as_number', ctypes.POINTER(PyAsNumber))
]


class EMailAddress:
    def __init__(self, address, domain):
        self.recipient = address + "@" + domain
        self.sender = None

    def __rshift__(self, other_address):
        self.sender = self.recipient
        self.recipient = other_address.recipient
        return self

    def mime(self, content="", subject=None):
        message = MIMEText(content)
        if subject:
            message["Subject"] = subject

        message["From"] = self.sender or "anyone@anywhere.fr"
        message["To"] = self.recipient

        return message

    def send(self, content, subject=None):
        message = self.mime(content, subject)

        with SMTP("localhost") as smtp:
            smtp.send_message(message)

    def __or__(self, arg):
        if isinstance(arg, dict):
            for subject, content in arg.items():
                self.send(content, subject)
                return self

        return self

    def __str__(self):
        return str(self.mime())

    def __repr__(self):
        return repr(self.mime())



def mulmat(address, domain):
    return EMailAddress(address, domain)

Str = PyUnicodeType.from_address(id(str))

p_tp_as_number = Str.tp_as_number
tp_as_number = p_tp_as_number[0]
tp_as_number.nb_matrix_multiply = AtBinOp(mulmat)


"samuel.charron" @ "data-publica.com" >> "samuel.charron" @ "c-radar.com" | {
    "Sujet":
    "Ca marche ?"
}
