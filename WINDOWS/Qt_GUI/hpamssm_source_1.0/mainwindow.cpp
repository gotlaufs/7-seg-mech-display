#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QFileInfo>


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_send_clicked()
{
    QString error = "";
    QString prog = QDir::currentPath() + "\\a.exe";
    QFileInfo check_file(prog);
    if(check_file.exists() == false){
        error = error + "Cant't open " + prog + "!<br>a.exe is lost from root directory!<br>";
    }
    QStringList params;
    params << "COM" + QString::number(ui->spinBox_comport->value()) << ui->lineEdit_message->text();
    if(params.size() != 2){
        error = error + "There is not enought parametrs for programm!<br>";
    }
    if(ui->lineEdit_message->text() == ""){
        error = error + "Message is too short!<br>";
    }
    QProcess *process = new QProcess(this);
    process->start(prog, params);
    process->waitForFinished(); // sets current thread to sleep and waits for pingProcess end
    QString output(process->readAll());
    if(output == ""){
        error = error + "Can't read answer from " + prog + "!<br>";
    }
    ui->textEdit_output->setText(ui->textEdit_output->toHtml() + "<font color='red'>Running:</font> " + prog + " " + params[0] + " \"" + params[1] + "\"<br>" + error + "<br>" + output);
}
