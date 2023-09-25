from PyQt6.QtWidgets import QLabel, QPushButton, QWidget,QApplication,QHBoxLayout,QVBoxLayout, QLineEdit,QFileDialog,QComboBox,QGroupBox
import sys
from ExcelToPsql import *
from DBConn import ConnectDb,GetTableInfo,InsertRegisters


class Main(QWidget):
    def __init__(self):

        super().__init__()


        self.connected_table=False
        self.openend_file=False
        self.enableMigrate = False


        self.setWindowTitle('Excel Records exporter to PSQL DataBase')

        MainLayout = QVBoxLayout()
        GetGeneralInfoSection = QVBoxLayout()
        DisplayInfoSection = QVBoxLayout()
        MigrationSection = QVBoxLayout()

        #MigrationSection Items
        self.MigrationFieldSection = QVBoxLayout()
        self.BtnMigrateSection = QHBoxLayout()

        #GetGeneralInfoSection Items
        FileRowInput = QHBoxLayout()
        DBNameInputRow = QHBoxLayout()
        TableNameInputRow = QHBoxLayout()

        #DisplayInfoSectionItems
        InfoSection = QHBoxLayout()
        self.FileHeaderSection = QVBoxLayout()
        self.DBColNameSection = QVBoxLayout()
        BtnStartMigrationSection = QHBoxLayout()

        #FileRowInput Items:
        FileNameLabel = QLabel("File Name (.xls)")
        self.FileImportFile = QPushButton("Search File")
        self.FileImportFile.clicked.connect(self.OpenFile)
        #layout all that Section
        FileRowInput.addStretch(1)
        FileRowInput.addWidget(FileNameLabel)
        FileRowInput.addWidget(self.FileImportFile)
        FileRowInput.addStretch(1)

        #DBNameInputRow Items:
        DBNameLabel = QLabel("DataBase Name")
        self.DBNameInput = QLineEdit()
        btnDBConnect = QPushButton("Connect")
        #layout all that Section
        DBNameInputRow.addStretch(1)
        DBNameInputRow.addWidget(DBNameLabel)
        DBNameInputRow.addWidget(self.DBNameInput)
        DBNameInputRow.addWidget(btnDBConnect)
        btnDBConnect.clicked.connect(self.Connect_db)
        DBNameInputRow.addStretch(1)

        #TableNameInputRow Items:
        self.TableNameLabel = QLabel("Table Name: ")
        self.TableNameInput = QLineEdit()
        self.btnTableGetInfo = QPushButton("Search Info")
        #Init status
        self.TableNameLabel.setEnabled(False)
        self.TableNameInput.setEnabled(False)
        self.btnTableGetInfo.setEnabled(False)
        #layout all that section
        TableNameInputRow.addStretch(1)
        TableNameInputRow.addWidget(self.TableNameLabel)
        TableNameInputRow.addWidget(self.TableNameInput)
        TableNameInputRow.addWidget(self.btnTableGetInfo)
        self.btnTableGetInfo.clicked.connect(self.getTableInfo)
        TableNameInputRow.addStretch(1)

        #GetGenralInfo Layout
        self.BtnStartMigration = QPushButton("Start Migration")
        self.BtnStartMigration.setEnabled(False)
        self.BtnStartMigration.clicked.connect(self.startMigration)
        BtnStartMigrationSection.addWidget(self.BtnStartMigration)

        self.BtnMigrate = QPushButton("Migrate")
        self.BtnMigrateSection.addWidget(self.BtnMigrate)
        self.BtnMigrate.setEnabled(False)
        self.BtnMigrate.clicked.connect(self.Migrate)

        #MigrationSection 
        MigrationSection.addStretch(1)
        MigrationSection.addLayout(self.MigrationFieldSection)
        MigrationSection.addLayout(self.BtnMigrateSection)
        MigrationSection.addStretch(1)

        GetGeneralInfoSection.addLayout(FileRowInput)
        GetGeneralInfoSection.addLayout(DBNameInputRow)
        GetGeneralInfoSection.addLayout(TableNameInputRow)

        InfoSection.addLayout(self.FileHeaderSection)
        InfoSection.addLayout(self.DBColNameSection)
        DisplayInfoSection.addStretch(1)
        DisplayInfoSection.addLayout(InfoSection)
        DisplayInfoSection.addLayout(BtnStartMigrationSection)
        DisplayInfoSection.addStretch(1)

        MainLayout.addLayout(GetGeneralInfoSection)
        MainLayout.addLayout(DisplayInfoSection)
        MainLayout.addLayout(MigrationSection)

        self.labelWidgets = []
        self.ColName = []
        self.col = []
        self.titles = []
        self.rows = []
        self.qcomboOption = []
        self.setLayout(MainLayout)

    def OpenFile(self):
        self.labelWidgets = []
        # print(self.DBColNameSection.count())
        for i in reversed(range(self.FileHeaderSection.count())):
            widget = self.FileHeaderSection.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        FileDialog = QFileDialog(self)
        options = FileDialog.options()
        selected_file, _= FileDialog.getOpenFileName(
            self,
            "Open Excel File",
            "",#Set the initial directory
            "Excel Files (*.xlsx);;All Files (*)",
            options=options
        )
        if selected_file:
            try:
                self.titles = []
                info = getData(selected_file)
                self.dbQueryValues = info['str-db']
                # print(info)
                headers = info['headers']
                # print(headers)
                for head in headers:
                    # print(type(head))
                    self.label = QLabel(head)
                    self.FileHeaderSection.addWidget(self.label)
                    self.labelWidgets.append(self.label)
                    self.titles.append(head)
                self.openend_file = True
                if self.openend_file and self.connected_table:
                    self.BtnStartMigration.setEnabled(True)
            except Exception as e:
                print("Error ",str(e))

    def Connect_db(self):

        dbName = self.DBNameInput.text()
        self.connectionStatus = ConnectDb(dbName)
        if self.connectionStatus:
            self.TableNameInput.setEnabled(True)
            self.TableNameLabel.setEnabled(True)
            self.btnTableGetInfo.setEnabled(True)

    
    def getTableInfo(self):
        for i in reversed(range(self.DBColNameSection.count())):
            widget = self.DBColNameSection.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.ColName = []
        tableName = self.TableNameInput.text()
        result = GetTableInfo(tableName)
        for cols in result:
            # print(type(cols))
            # print(cols)
            self.col.append(cols[0])
            col_info = f'Name: {cols[0]} {cols[1]}({cols[2]}) DEFAULT VALUE {cols[3]} '
            self.label_cols = QLabel(col_info)
            self.DBColNameSection.addWidget(self.label_cols)
            self.ColName.append(self.label_cols)
        self.connected_table = True

        if self.connected_table and self.openend_file:
            self.BtnStartMigration.setEnabled(True)
# # 
    def startMigration(self):
        self.clearRows()
        self.qcomboOption = []
        # self.parent = QVBoxLayout()
        # self.MigrationFieldSection.addLayout(self.parent)
        for title in self.titles:
            # self.row = QHBoxLayout()
            self.rowLabel = QLabel(title)
            # self.MigrationFieldSection.addWidget(self.rowLabel)
            self.row.append(title)

            self.rowLayout = QHBoxLayout()
            self.comboOptions = QComboBox()
            self.comboOptions.addItems(self.col)

            self.rowLayout.addStretch(1)
            self.rowLayout.addWidget(self.rowLabel)
            self.rowLayout.addStretch(1)
            self.rowLayout.addWidget(self.comboOptions)
            self.rowLayout.addStretch(1)

            self.group = QGroupBox()
            self.qcomboOption.append(self.comboOptions)
            self.group.setLayout(self.rowLayout)
            

            self.MigrationFieldSection.addWidget(self.group)

            # self.row.addWidget(self.rowLabel)
            # self.MigrationSection.addLayout(self.row)
            # print(f'Titles: {title}')
            # self.rows.append(self.row)
            # self.op = QComboBox()
            # self.op.addItems(self.col)
            # self.row.addStretch(1)
            # self.row.addWidget(self.op)
            # self.qcomboOption.append(self.op)
            # self.group = QGroupBox()
            # self.group.setLayout(self.row)
            # self.parent.addLayout(self.row)
        # self.MigrationFieldSection.addWidget(self.btn_migrate)
        self.enableMigrate = True
        self.BtnMigrate.setEnabled(True)
    def clearRows(self):
        self.row = []
        for i in reversed(range(self.MigrationFieldSection.count())):
            widget = self.MigrationFieldSection.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def Migrate(self):
        i = 0
        str_field = '('
        tablename = self.TableNameInput.text()
        # print("Execute QUERY")
        for qcombo in self.qcomboOption:
            txt = qcombo.currentText()
            if i == (len(self.qcomboOption) - 1):
                print('es el ultimo elemento')
                str_field = str_field + txt + ')'
            else:
                print('No es el ultimo elemento')
                str_field = str_field + txt + ','
            i = i +1
        
        print(str_field)
            # print(qcombo.currentText())
        print('------------------------')
        print(self.dbQueryValues)
        query = f"INSERT INTO {tablename} {str_field} VALUES {self.dbQueryValues}"
        print(query)
        InsertRegisters(query,self.DBNameInput.text())
        # for head in self.titles:
        #     print(head)
#         i = 
#         str_fields = '('
#         print(len(self.qcomboOption))

#         for fields in self.qcomboOption:
#             txt = fields.currentText()
#             if i == (len(self.qcomboOption) - 1):
#                 print("Es el ultimo elemento")
#             else:
#                 print("No es el ultimo")
#             i = i + 1
#             # str_fields = str_fields + txt + ','
#         str_fields = str_fields + ')'
#         # first_text = self.qcomboOption[0]
#         # first_text = first_text.currentText()
#         print(str_fields)

app = QApplication(sys.argv)
wind = Main()
wind.show()

app.exec()