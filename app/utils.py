import re
import logging, datetime


def kenyatime():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=3)


class ParseError(ValueError):
    def __init__(self):
        self.message = "Could Not Parse This Message. Message Maybe malformed"


def parse_message(message: str) -> dict:
    """Parse Mpesa Messages to extract usefull info
    :keyword message: Messsage blob
    :type message: str
    :param transactionID: Unique Transaction ID genearted by Mpesa
    :param transactionCost: Cost of Transaction
    :type transactionCost: .2f
    :param amount: Amount being transacted
    :type amount: .2f
    :param status: Status of a given Transaction
    :rtype: dict
    :raises ParseError
    >>> p = parse_message(message="LL51J4JPIB Confirmed. Ksh577.00 sent to STEPHEN KAMAU 0722279605 on 5/12/17 at 2:04 PM. New M-PESA balance is Ksh421.00. Transaction cost, Ksh15.00")
    >>> p == {'transactionID': 'LL51J4JPIB', 'status': 'Confirmed', 'amount': 'Ksh577.00','description': 'Ksh577.00 sent to STEPHEN KAMAU 0722279605 on 5/12/17 at 2:04 PM','transactionCost': 'Ksh15.00','phoneNumber': '0722279605'}
    True
    """
    if message is None: raise ParseError

    # remove white spaces from message
    stripedMsg = []
    list(map(lambda x: stripedMsg.append(x), message.split()))
    formatted_message = ''.join(stripedMsg)

    # get status and transactionID
    status_transRegex = re.compile(r'(.*)(Confirmed|Failed)')
    mo = status_transRegex.search(formatted_message)
    if mo is None: raise ParseError
    transactionId, status = mo.groups()

    # get phoneNumber
    phoneNumRegex = re.compile(r'(07|\+2547)\d{8}')
    mo = phoneNumRegex.search(formatted_message)
    phoneNumber = ''
    if mo is not None: phoneNumber = mo.group()


    # get amount
    amountRegex = re.compile(r'Ksh(\d+.00)')
    mo = amountRegex.search(formatted_message)
    if mo is None: raise ParseError
    amount = mo.group()

    # get transaction cost
    tsc = message.split('. ')[-1]
    mo = amountRegex.search(tsc)
    transactionCost = 0
    if mo is not None: transactionCost = mo.group()

    return {
        'transactionID': transactionId,
        'status': status,
        'amount': amount,
        'description': message.split('. ')[1],
        'transactionCost': transactionCost,
        'phoneNumber': phoneNumber
    }


# if __name__ == '__main__':
# """Run Doctests"""
#     import doctest
#     doctest.testmod()
