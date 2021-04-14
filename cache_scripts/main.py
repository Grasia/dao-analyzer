import daostack.main as daostack
import daohaus.main as daohaus
import aragon.main as aragon

from datetime import date
import os

if __name__ == '__main__':
    daostack.run()
    daohaus.run()
    aragon.run()

    # write date
    data_date: str = str(date.today())

    with open(os.path.join('datawarehouse', 'update_date.txt'),'w') as f:
        f.write(data_date)
