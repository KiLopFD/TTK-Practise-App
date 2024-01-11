import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import DatePickerDialog, MessageDialog
from ttkbootstrap.widgets import DateEntry
from src.model.crud import (
    create_user,
    get_all_users,
    delete_user,
    delete_all,
    up_user
)
from datetime import datetime
from ttkbootstrap.tableview import Tableview
from src.utils.validation import(
    ValidationUtils
)


class BaseApp(ttk.Frame):
    def __init__(self, master: ttk.Window, **kw):
        super().__init__(master=master,**kw)
        self.pack(fill=BOTH, expand=True)
        self.name_var = ttk.StringVar(value="")
        self.address_var = ttk.StringVar(value="")
        self.cmnd_var = ttk.StringVar(value="")
        self.date_var = ttk.StringVar(value="")
        self.id_user = ttk.IntVar(value=0)
        self.date_pick = None
        self.frame_two = None
        self.create_widgets()
        self.dt=None
        self.create_table()
    
    def create_widgets(self):
        self.create_base_frame()

    def create_base_frame(self):
        label_logo = ttk.Label(self, text="Full House DEV", font=("Arial", 20))
        label_logo.pack(fill=X, padx=10, pady=10)
        container = ttk.Frame(self, padding=10)
        container.pack()
        col_base_one = ttk.Frame(container, padding=10)
        col_base_one.grid(row=0, column=0)
        col_base_two = ttk.Frame(container, padding=10)
        col_base_two.grid(row=0, column=1) 
        # col_base_one implementation
        # Name:
        ctn_name = ttk.Frame(col_base_one, padding=10)
        ctn_name.pack()
        label_name = ttk.Label(ctn_name, text="Name", width=10)
        label_name.pack(side=LEFT, padx=10)
        entry_name = ttk.Entry(ctn_name, width=24, textvariable=self.name_var)
        entry_name.pack(fill=X)
        # Address:
        ctn_address = ttk.Frame(col_base_one, padding=10)
        ctn_address.pack()
        label_address = ttk.Label(ctn_address, text="Address", width=10)
        label_address.pack(side=LEFT, padx=10)
        entry_address = ttk.Entry(ctn_address, width=24, textvariable=self.address_var)
        entry_address.pack(fill=X)
        # CMND:
        ctn_cmnd = ttk.Frame(col_base_one, padding=10)
        ctn_cmnd.pack()
        label_cmnd = ttk.Label(ctn_cmnd, text="CMND", width=10)
        label_cmnd.pack(side=LEFT, padx=10)
        entry_cmnd = ttk.Entry(ctn_cmnd, width=24, textvariable=self.cmnd_var)
        entry_cmnd.pack(fill=X)
        # Set ID
        ctn_id = ttk.Frame(col_base_one, padding=10)
        ctn_id.pack()
        label_id = ttk.Label(ctn_id, text="ID", width=10)
        label_id.pack(side=LEFT, padx=10)
        entry_id = ttk.Entry(ctn_id, width=24, textvariable=self.id_user)
        entry_id.pack(fill=X)
        # Date
        ctn_date = ttk.Frame(col_base_one, padding=10)
        ctn_date.pack()
        label_date = ttk.Label(ctn_date, text="Date", width=10)
        label_date.pack(side=LEFT, padx=10)
        self.date_pick = ttk.DateEntry(ctn_date)
        self.date_pick.pack(fill=X)
        # date_pick.bind("<<DateEntrySelected>>", set_date)
        # group button:
        ctn_button = ttk.LabelFrame(col_base_one, text="Group Actions")
        ctn_button.pack(fill=X)
        button_add = ttk.Button(ctn_button, text="Add", command=self.add_action)
        button_add.pack(side=LEFT, padx=10, pady=10)
        button_delete = ttk.Button(ctn_button, text="Delete", command=self.delete_action)
        button_delete.pack(side=LEFT, padx=10, pady=10)
        button_edit = ttk.Button(ctn_button, text="Edit", command=self.update)
        button_edit.pack(side=LEFT, padx=10, pady=10)
        # label notice:
        label_notice = ttk.Label(col_base_one, text="Notice: ")
        label_notice.pack(fill=X, padx=10, pady=10)
        # open new window
        button_create_new_window = ttk.Button(col_base_one, text="Create Form", command=self.create_new_window)
        button_create_new_window.pack(side=LEFT, padx=10, pady=10)
        # def show_notice():
        #     label_notice.config(text=f"Notice: {date_pick.entry.get()}")
        # col_base_two
        self.frame_two = ttk.LabelFrame(col_base_two, text="Data View", padding=20)
        self.frame_two.pack(fill=BOTH, expand=True)
        # Validation:
        ValidationUtils.validate_nullable(entry_name)
        
        
    def create_new_window(self):
        config_window = {
            "title": "teacher",
            "themename": "litera",
            "size": (1500, 600),
            "position": (100, 100),
            "resizable": (False, False),
        }
        # title: str = "ttkbootstrap",
        # themename: str = "litera",
        # iconphoto: str = '',
        # size: Any | None = None,
        # position: Any | None = None,
        # minsize: Any | None = None,
        # maxsize: Any | None = None,
        # resizable: Any | None = None,
        # hdpi: bool = True,
        # scaling: Any | None = None,
        # transient: Any | None = None
        window = ttk.Window(**config_window)
        BaseApp(window)
        window.mainloop()
    
    def add_action(self):
        if ValidationUtils.check_state:
            user = create_user(self.name_var.get(), self.address_var.get(), self.cmnd_var.get(), datetime.strptime(self.date_pick.entry.get(), "%m/%d/%Y"))
            self.dt.insert_row(index='end',values=[user.id, self.name_var.get(), self.address_var.get(), self.cmnd_var.get(), self.date_pick.entry.get()])
            self.dt.load_table_data()
        else:
            mess = MessageDialog(title="Error Add Action", message="Please check your input", style='error', alert=True)
            mess.show()
        
    def delete_action(self):
        id = self.id_user.get()
        if id == None or id not in [item.id for item in get_all_users()]:
            delete_all()
            self.dt.delete_rows()
            self.dt.load_table_data()
            return
        delete_user(id)
        self.dt.build_table_data(['Id','Name', 'Address', 'CMND', 'Date'], [
            (item.id, item.name, item.address, item.cmnd, item.date)
            for item
            in get_all_users()
        ])
        self.dt.load_table_data()    
        
    def update(self) -> None:
        id_user = self.id_user.get()
        check_exist = id_user in [item.id for item in get_all_users()]
        if check_exist:
            up_user(id_user, self.name_var.get(), self.address_var.get(), self.cmnd_var.get(), datetime.strptime(self.date_pick.entry.get(), "%m/%d/%Y"))
            self.dt.delete_rows()
            self.dt.load_table_data()
            self.dt.insert_rows(index='end', rowdata=[
                (item.id, item.name, item.address, item.cmnd, item.date)
                for item
                in get_all_users()
            ])
            self.dt.load_table_data()
        
            
    def create_table(self):
        coldata = ['Id','Name', 'Address', 'CMND', 'Date']
        rowdata = [
            (item.id, item.name, item.address, item.cmnd, item.date)
            for item
            in get_all_users()
        ]

        self.dt = Tableview(
            master=self.frame_two,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
        )
        self.dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    


if __name__ == '__main__':
    config_window = {
        "title": "student",
        "themename": "litera",
        "size": (1500, 600),
        "position": (100, 100),
        "resizable": (False, False),
    }
    # title: str = "ttkbootstrap",
    # themename: str = "litera",
    # iconphoto: str = '',
    # size: Any | None = None,
    # position: Any | None = None,
    # minsize: Any | None = None,
    # maxsize: Any | None = None,
    # resizable: Any | None = None,
    # hdpi: bool = True,
    # scaling: Any | None = None,
    # transient: Any | None = None
    window = ttk.Window(**config_window)
    BaseApp(window)
    window.mainloop()