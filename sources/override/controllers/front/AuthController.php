<?php
class AuthController extends AuthControllerCore
{
    protected function makeCustomerFormatter()
    {
        $formatter = parent::makeCustomerFormatter();
        
        $formatter
            ->setAskForPartnerOptin(false)
            ->setAskForBirthdate(false)
            ->setPartnerOptinRequired(false);

        return $formatter;
    }
}

