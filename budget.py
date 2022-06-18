class Category:
  '''
  A class to represent a category of the budget like food, electronics, etc

  ...

  Attributes
  ----------
  description : str
    
  Methods
  -------
  deposit(amount, description="")

  withdrawl(amount, description="")

  get_balance()

  transfer(amount, targ_category)

  check_funds(amount)
  
  
  '''
  
  def __init__(self, description):
    '''
    Constructs the category for the budget
    
    Parameters
    ----------
      description : str
        description of the transaction
    '''
    self.description = description
    self.ledger = []
    self.__balance = 0.0

  
  def __repr__(self):
    '''
    Function to return printable representation of the Category 
    '''
    header = self.description.center(30, '*') + '\n'
    ledger = ''
    for item in self.ledger:
      # Maintain formatting standards set by Instructions
      description_line = '{:<23}'.format(item['description'])
      amount_line = '{:7.2f}'.format(item['amount'])
      ledger += '{}{}\n'.format(description_line[:23], amount_line[:7])
    total_line = 'Total: {:.2f}'.format(self.__balance)
    return header + ledger + total_line
      

  def deposit(self, amount, description=""):
    '''
    Deposit an amount into the budget category
    
    Parameters
    ----------
      amount : float
        amount associated with the transaction
      description : str
        description of the transaction
    
    Returns
    -------
    None
    '''
    self.ledger.append({'amount': amount, 'description': description})
    self.__balance += amount

    
  def withdraw(self, amount, description=""):
    '''
    Withdraw an amount from a budget category
    
    Parameters
    ----------
      amount : float
        amount associated with the transaction
      description : str
        description of the transaction
    
    Returns
    -------
    Boolean 
      True if withdrawl completed
      False if withdrawl could not be completed
    '''
    if self.__balance >= amount:
      self.ledger.append({'amount': -1 * amount, 'description': description})
      self.__balance -= amount
      return True
    else: return False
      

  def get_balance(self):
    '''
    Deposit an amount into the budget category
    
    Returns
    -------
    Category Balance : float
    '''
    return self.__balance

  
  def transfer(self, amount, targ_category):
    '''
    Transfer an amount from category into another budget category
    
    Parameters
    ----------
      amount : float
        amount associated with the transaction
      targ_category : str
        Target budget category for transfer
    
    Returns
    -------
    Boolean
      True
      False
    '''
    if self.withdraw(amount, 'Transfer to {0}'.format(targ_category.description)):
      targ_category.deposit(amount, 'Transfer from {0}'.format(self.description))
      return True
    else: return False

  
  def check_funds(self, amount):
    '''
    Check funds of the category to see if transaction possible 
    
    Parameters
    ----------
      amount : float
        amount associated with the transaction
    
    Returns
    -------
    Boolean
      True
      False
    '''
    if self.__balance >= amount: return True
    else: return False




def create_spend_chart(categories):
  '''
  Creates the spending chart for all budget categories
  
  Parameters
  ----------
    categories : list
      list of budget categories
  
  Returns
  -------
  String
  '''
  withdrawls = []
  for cat in categories:
    balance = 0
    for item in cat.ledger:
      if item['amount'] < 0:
        balance += abs(item['amount'])
    withdrawls.append(round(balance, 2))

  percent_spent = list(map(lambda amount: int((((amount/round(sum(withdrawls), 2)) * 10) // 1) * 10), withdrawls))
  
  chart_header = 'Percentage spent by category\n'
  
  chart_body = ''
  for value in range(100, -1, -10):
    chart_body += '{0}'.format(value).rjust(3) + '|'
    for percent in percent_spent:
      if percent >= value: chart_body += ' o '
      else: chart_body += '   '
    chart_body += ' \n'
  
  chart_footer = '    ' + '-' * ((3 * len(categories)) + 1) + '\n'
  
  descs = list(map(lambda cat: cat.description, categories))
  max_descs_length = max(map(lambda desc: len(desc), descs))
  
  upd_descs = list(map(lambda desc: desc.ljust(max_descs_length), descs))

  for x in zip(*upd_descs):
    chart_footer += '    ' + ''.join(map(lambda s: s.center(3), x)) + ' \n'

  return (chart_header + chart_body + chart_footer).rstrip('\n')
