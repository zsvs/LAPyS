<?php
class FirstClass
{
    protected $handleOpen;
    protected $handleRead;
    protected $fileName;
    protected $contentFile;

    public function __construct($fileName)
    {
        if(!is_writable("Kernel-LAPyS/Files/" . $fileName . '.txt')){
            echo "Файл '$fileName' недоступен для записи";
            exit;
        }
        if(!fopen("Kernel-LAPyS/Files/" . $fileName . '.txt', "a")){
            echo "Не могу открыть файл ($fileName)";
            exit;
        }

       $this->handleOpen = fopen("Kernel-LAPyS/Files/" . $fileName . '.txt', "a");
       $this->handleRead = fopen("Kernel-LAPyS/Files/" . $fileName . '.txt', "r+");
       $this->fileName = $fileName;
    }

    public function __destruct()
    {
        if(is_writable($this->fileName))
        {
            fclose($this->handleOpen);
        }
    }


    public function fillFile($text){
        if (fwrite($this->handleOpen, $text) === false) {
            echo "Не могу произвести запись в файл ($this->fileName)";
            exit;
        }
//        echo "Текст: '$text', успешно записан! <br>";
    }

    public function readFile(){
        if(filesize("Kernel-LAPyS/Files/" . $this->fileName . '.txt') == 0){
            return "Файл пуст!";
        }else{
            $this->contentFile = fread($this->handleRead, filesize("Kernel-LAPyS/Files/" . $this->fileName . '.txt'));
            //ftruncate($this->handleRead, 0);
            echo $this->contentFile;
        }
    }

    public function clearFile(){
        if(!$this->handleRead){
            echo "Не могу открыть файл ($this->fileName)";
            exit;
        }
        ftruncate($this->handleRead, 0);
    }

}
