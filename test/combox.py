import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MyCustomDialog(QDialog):
    def __init__(self, app=None, parent=None):
        QDialog.__init__(self, parent)

        self.app = app

        # Second, we need our QTreeView() and
        # the settings
        self.init_tree_view()

        # Create an empty model for the TreeViews' data
        _standard_item_model = QStandardItemModel(0, 2)

        # Add some textual items
        self.food_list = [
            ["0", 'Cookie dough'],
            ["1", 'Hummus'],
            ["2", 'Spaghetti'],
            ["3", 'Dal makhani'],
            ["6", 'Blolonese'],
            ["4", 'Hachfleisch'],
            ["3", 'Nudeln'],
            ["3", 'Fleisch'],
            ["4", 'Chocolate whipped cream']
        ]
        # Now its time to populate data
        self.populate(model=_standard_item_model)

        # Well we also want to set the header
        # self.set_header_data(list_header_data = ["ID", "Genre"], model=_standard_item_model)

        # Apply the model to the list view
        self.set_tree_view_model(_standard_item_model)

        # QComboBox() will be created
        self.combo_box = QComboBox(self)

        # we have to initialize the QComboBox()
        self.init_combo(model=_standard_item_model)

        # set the selectionChanged to QTreeView()
        self.selection_changed()

        # layout is a defined QVBoxLayout()
        layout = QVBoxLayout(self)
        layout.addWidget(self.combo_box)
        self.setLayout(layout)

    def init_tree_view(self):
        self.tree_view = QTreeView()
        self.tree_view.setRootIsDecorated(False)
        self.tree_view.setWordWrap(True)

        self.tree_view.setAlternatingRowColors(True)

        self.tree_view.setSelectionMode(QTreeView.ExtendedSelection)

        self.tree_view.header().hide()

    def set_text_ff_completer_is_clicked(self, text):
        '''
            On selection of an item from the completer,
            select the corresponding item from combobox
        '''
        if text:
            index = self.combo_box.findText(text)
            print
            "text", text
            self.combo_box.setCurrentIndex(index)

    def set_tree_view_model(self, model):

        self.tree_view.setModel(model)

    def init_combo(self, model=None):

        self.combo_box.setModel(model)
        self.combo_box.setView(self.tree_view)

        # self.combo_box.setMaxVisibleItems(5)

        # self.combo_box.setEditable(True)

        self.combo_box.currentIndexChanged.connect(lambda: self.on_combo_box_changed(tree_view=self.tree_view))

        # self.combo_box.currentIndexChanged[int].connect(self.on_combo_box_changed)

        self.tree_view.resizeColumnToContents(0)
        self.tree_view.setColumnHidden(1, True)

        # self.combo_box.setModelColumn(1);
        # self.combo_box.setCurrentIndex(index);

        self.combo_box.setCurrentIndex(6)

    def on_combo_box_changed(self, tree_view=None):
        '''display text of selected item '''
        # Get the index first
        indexes = tree_view.selectedIndexes()

        if len(indexes) > 0:

            indexy = indexes[0].data()  # data method of QModelIndex is a
            # convenient method. It returns a QVariant.
            # For getting the
            # display text for that particular index
            # you have to use the toString()-method

            # Next step. convert information
            if isinstance(indexy, QVariant):
                print
                "indexy", indexy.toString()

    def selection_changed(self):

        self.tree_view.selectionModel().selectionChanged.connect(lambda new_index:
                                                                 self.get_id_tree_view(new_index=new_index))

    def generator_header_data(self, list_header):

        for header_data in list_header:
            yield header_data

    def set_header_data(self, list_header_data=None, model=None):

        count_column = 0

        for header_data in self.generator_header_data(list_header_data):
            model.setHeaderData(count_column, Qt.Horizontal, header_data)

            count_column += 1

    def get_id_tree_view(self, new_index=None):

        try:
            if not new_index is None:

                index = new_index.indexes()[1].data()  # .toPyObject()

                if isinstance(index, QVariant):
                    print
                    "index", index.toString()

        except IndexError as InErr:
            pass  # print "InErr", InErr

    def populate_data_item(self, item_list=None, model=None):

        count_items = len(item_list)

        if count_items == 2:
            item_first, item_second = item_list

        two_columns_item = [QStandardItem(item_second), QStandardItem(str(item_first))]

        model.appendRow(two_columns_item)

    def populate(self, model=None):

        for single_list in self.food_list:
            self.populate_data_item(item_list=single_list, model=model)


def main():
    app = QApplication(sys.argv)
    window = MyCustomDialog(app=app)
    window.resize(300, 50)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()