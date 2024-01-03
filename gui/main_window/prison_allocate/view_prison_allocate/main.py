from logging import disable
from pathlib import Path
import controller as db_controller

from tkinter import (
    Frame,
    Canvas,
    Entry,
    Text,
    Button,
    PhotoImage,
    messagebox,
    StringVar,
)
from tkinter.ttk import Treeview

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def view_prison_allocate():
    ViewPrisonAllocate()


class ViewPrisonAllocate(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.search_query = StringVar()
        self.prison_allocate_data = None

        self.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=432,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            40.0, 14.0, 742.0, 16.0, fill="#EFEFEF", outline=""
        )

        self.canvas.create_rectangle(
            40.0, 342.0, 742.0, 344.0, fill="#EFEFEF", outline=""
        )

        self.canvas.create_text(
            116.0,
            33.0,
            anchor="nw",
            text="View Prison Allocate",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.canvas.create_text(
            40.0,
            367.0,
            anchor="nw",
            text="Avail. Actions:",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.canvas.create_text(
            116.0,
            65.0,
            anchor="nw",
            text="And Perform Operations",
            fill="#808080",
            font=("Montserrat SemiBold", 16 * -1),
        )

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(666.0, 59.0, image=self.image_image_1)

        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(680.5, 60.0, image=self.entry_image_1)
        entry_1 = Entry(
            self,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            foreground="#777777",
            font=("Montserrat Bold", 18 * -1),
            textvariable=self.search_query,
        )
        # Bind text change to function
        entry_1.bind(
            "<KeyRelease>",
            lambda event: self.filter_treeview_records(self.search_query.get()),
        )

        entry_1.place(x=637.0, y=48.0, width=87.0, height=22.0)

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.refresh_btn = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_refresh,
            relief="flat",
        )
        self.refresh_btn.place(x=525.0, y=33.0, width=53.0, height=53.0)

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        image_2 = self.canvas.create_image(617.0, 60.0, image=self.image_image_2)

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        self.navigate_back_btn = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_navigate_back,
            relief="flat",
        )
        self.navigate_back_btn.place(x=40.0, y=33.0, width=53.0, height=53.0)

        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        self.delete_btn = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_delete,
            relief="flat",
            state="disabled",
        )

        self.delete_btn.place(x=596.0, y=359.0, width=146.0, height=48.0)

        self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        self.edit_btn = Button(
            self,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_edit,
            relief="flat",
            state="disabled",
        )
        self.edit_btn.place(x=463.0, y=359.0, width=116.0, height=48.0)

        # self.canvas.create_rectangle(
        #     40.0,
        #     101.0,
        #     742.0,
        #     329.0,
        #     fill="#EFEFEF",
        #     outline="")
        # Add treeview here

        self.columns = {
            "pa": "PreAl. ID",
            "Pres": "Prisoners ID",
            "pre_son": "Prison ID",
            "a_t": "Allocate Time",
            "r_t": "Released Time",
            "supp": "Supplies",
            "sta": "Status",
        }

        self.treeview = Treeview(
            self,
            columns=list(self.columns.keys()),
            show="headings",
            height=200,
            selectmode="browse",
            # ="#FFFFFF",
            # fg="#5E95FF",
            # font=("Montserrat Bold", 18 * -1)
        )

        # Show the headings
        self.treeview.heading(list(self.columns.keys())[0], text="PreAl")
        self.treeview.heading(list(self.columns.keys())[1], text="Prisoners ID")
        self.treeview.heading(list(self.columns.keys())[2], text="Prison Cell ID")
        self.treeview.heading(list(self.columns.keys())[3], text="Allocate")
        self.treeview.heading(list(self.columns.keys())[4], text="Released")
        self.treeview.heading(list(self.columns.keys())[5], text="Supplies")
        self.treeview.heading(list(self.columns.keys())[6], text="Status")
        # Set the column widths
        self.treeview.column(list(self.columns.keys())[0], width=50)
        self.treeview.column(list(self.columns.keys())[1], width=50)
        self.treeview.column(list(self.columns.keys())[2], width=50)
        self.treeview.column(list(self.columns.keys())[3], width=150)
        self.treeview.column(list(self.columns.keys())[4], width=150)
        self.treeview.column(list(self.columns.keys())[5], width=60)
        self.treeview.column(list(self.columns.keys())[6], width=100)
        # # Insert data from variable
        # if self.prison_allocate_data:
        #     for allocate prison in self.prison_allocate_data:
        #         self.treeview.insert('', 'end', values=allocate prison)

        self.treeview.place(x=40.0, y=101.0, width=700.0, height=229.0)

        # Insert data
        self.handle_refresh()

        # Add selection event
        self.treeview.bind("<<TreeviewSelect>>", self.on_treeview_select)

        # Add sample data
        self.button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
        self.checkout_btn = Button(
            self,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_checkout,
            relief="flat",
            state="disabled",
        )

        self.checkout_btn.place(x=272.0, y=359.0, width=174.0, height=48.0)

    def handle_checkout(self, event=None):
        if not self.parent.selected_pca_id:
            # Show warning
            messagebox.showwarning(
                "Select a allocate prison First", "Please select a prisoner to release"
            )
        # Get the selected allocate prison
        db_controller.R_eleased(self.parent.selected_pca_id)
        self.parent.refresh_entries()

    def filter_treeview_records(self, query):
        self.treeview.delete(*self.treeview.get_children())
        # run for loop from original data
        for row in self.prison_allocate_data:
            # Check if query exists in any value from data
            if query.lower() in str(row).lower():
                # Insert the data into the treeview
                self.treeview.insert("", "end", values=row)
        self.on_treeview_select()

    def on_treeview_select(self, event=None):
        try:
            self.treeview.selection()[0]
        except:
            self.parent.selected_pca_id = None
            return
        # Get the selected item
        item = self.treeview.selection()[0]
        # Get the allocate prison id
        self.parent.selected_pca_id = self.treeview.item(item, "values")[0]
        # Enable the buttons
        self.delete_btn.config(state="normal")
        self.edit_btn.config(state="normal")
        self.checkout_btn.config(state="normal")

    def handle_refresh(self):
        self.treeview.delete(*self.treeview.get_children())
        if self.prison_allocate_data:
            self.prison_allocate_data = db_controller.get_prison_allocate()
        else:
            self.prison_allocate_data = self.parent.prison_allocate_data

        for row in self.prison_allocate_data:
            self.treeview.insert("", "end", values=row)

        # Refresh the dashboard
        try: self.parent.parent.handle_dashboard_refresh()
        except: pass


    def handle_navigate_back(self):
        self.parent.navigate("add")

    def handle_delete(self):
        db_controller.delete_prison_allocate(self.parent.selected_pca_id)

    def handle_edit(self):
        self.parent.navigate("edit")
        self.parent.windows["edit"].initialize()
