
from menu import Menu

mymenu= Menu()

while(mymenu.user!=4):
    mymenu.login()
    if mymenu.user==2:
        mymenu.menu_for_student()
    elif mymenu.user==3:
        mymenu.menu_for_admin()
    
print("Goodbye.")        
