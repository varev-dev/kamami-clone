<?php
class CustomerFormatter extends CustomerFormatterCore
{
    public function getFormat()
    {
        $format = parent::getFormat();

        if (isset($format['id_gender'])) {
            unset($format['id_gender']);
        }

        return $format;
    }
}

