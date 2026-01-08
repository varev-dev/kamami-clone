<?php
class CustomerFormatter extends CustomerFormatterCore
{
    public function getFormat()
    {
        $format = parent::getFormat();

        if (isset($format['id_gender'])) {
            unset($format['id_gender']);
        }

        if (isset($format['psgdpr_psgdpr'])) {
            unset($format['psgdpr_psgdpr']);
        }

        return $format;
    }
}

