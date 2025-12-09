<?php
/**
 * Copyright since 2007 PrestaShop SA and Contributors
 * PrestaShop is an International Registered Trademark & Property of PrestaShop SA
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Academic Free License 3.0 (AFL-3.0)
 * that is bundled with this package in the file LICENSE.md.
 * It is also available through the world-wide-web at this URL:
 * https://opensource.org/licenses/AFL-3.0
 * If you did not receive a copy of the license and are unable to
 * obtain it through the world-wide-web, please send an email
 * to license@prestashop.com so we can send you a copy immediately.
 *
 * DISCLAIMER
 *
 * Do not edit or add to this file if you wish to upgrade PrestaShop to newer
 * versions in the future. If you wish to customize PrestaShop for your
 * needs please refer to https://devdocs.prestashop.com/ for more information.
 *
 * @author    PrestaShop SA and Contributors <contact@prestashop.com>
 * @copyright Since 2007 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License 3.0 (AFL-3.0)
 */
if (!defined('_PS_VERSION_')) {
    exit;
}

class Ps_SidebarNewProducts extends Module
{
    public function __construct()
    {
        $this->name = 'ps_sidebarnewproducts';
        $this->tab = 'front_office_features';
        $this->version = '1.0.0';
        $this->author = 'PrestaShop';
        $this->need_instance = 0;

        $this->bootstrap = true;
        parent::__construct();

        $this->displayName = $this->trans('Sidebar New Products', [], 'Modules.Sidebarnewproducts.Admin');
        $this->description = $this->trans('Displays new products in the left sidebar.', [], 'Modules.Sidebarnewproducts.Admin');
        $this->ps_versions_compliancy = ['min' => '1.7.1.0', 'max' => _PS_VERSION_];
    }

    public function install()
    {
        return parent::install()
            && $this->registerHook('displayLeftColumn')
            && Configuration::updateValue('PS_SIDEBAR_NEW_PRODUCTS_NBR', 8);
    }

    public function uninstall()
    {
        return Configuration::deleteByName('PS_SIDEBAR_NEW_PRODUCTS_NBR')
            && parent::uninstall();
    }

    public function getContent()
    {
        $output = '';

        if (Tools::isSubmit('submitPs_sidebarnewproducts')) {
            $nbr = (int) Tools::getValue('PS_SIDEBAR_NEW_PRODUCTS_NBR');
            if ($nbr <= 0) {
                $output .= $this->displayError($this->trans('Invalid number of products.', [], 'Modules.Sidebarnewproducts.Admin'));
            } else {
                Configuration::updateValue('PS_SIDEBAR_NEW_PRODUCTS_NBR', $nbr);
                $output .= $this->displayConfirmation($this->trans('Settings updated.', [], 'Admin.Notifications.Success'));
            }
        }

        return $output . $this->renderForm();
    }

    public function renderForm()
    {
        $fields_form = [
            'form' => [
                'legend' => [
                    'title' => $this->trans('Settings', [], 'Admin.Global'),
                    'icon' => 'icon-cogs',
                ],
                'input' => [
                    [
                        'type' => 'text',
                        'label' => $this->trans('Number of products to display', [], 'Modules.Sidebarnewproducts.Admin'),
                        'name' => 'PS_SIDEBAR_NEW_PRODUCTS_NBR',
                        'class' => 'fixed-width-xs',
                        'desc' => $this->trans('Set the number of products to be displayed in this block.', [], 'Modules.Sidebarnewproducts.Admin'),
                    ],
                ],
                'submit' => [
                    'title' => $this->trans('Save', [], 'Admin.Actions'),
                ],
            ],
        ];

        $helper = new HelperForm();
        $helper->show_toolbar = false;
        $helper->table = $this->table;
        $helper->module = $this;
        $helper->default_form_language = (int) Configuration::get('PS_LANG_DEFAULT');
        $helper->allow_employee_form_lang = Configuration::get('PS_BO_ALLOW_EMPLOYEE_FORM_LANG') ? Configuration::get('PS_BO_ALLOW_EMPLOYEE_FORM_LANG') : 0;
        $helper->identifier = $this->identifier;
        $helper->submit_action = 'submitPs_sidebarnewproducts';
        $helper->currentIndex = $this->context->link->getAdminLink('AdminModules', false)
            . '&configure=' . $this->name . '&tab_module=' . $this->tab . '&module_name=' . $this->name;
        $helper->token = Tools::getAdminTokenLite('AdminModules');
        $helper->tpl_vars = [
            'fields_value' => $this->getConfigFieldsValues(),
            'languages' => $this->context->controller->getLanguages(),
            'id_language' => $this->context->language->id,
        ];

        return $helper->generateForm([$fields_form]);
    }

    public function getConfigFieldsValues()
    {
        return [
            'PS_SIDEBAR_NEW_PRODUCTS_NBR' => Configuration::get('PS_SIDEBAR_NEW_PRODUCTS_NBR', 8),
        ];
    }

    public function hookDisplayLeftColumn($params)
    {
        if (!Configuration::get('PS_CATALOG_MODE')) {
            $products = $this->getNewProducts();
            if (!$products) {
                return;
            }

            $this->context->smarty->assign([
                'products' => $products,
                'allNewProductsLink' => $this->context->link->getPageLink('new-products', true),
            ]);

            return $this->display(__FILE__, 'views/templates/hook/ps_sidebarnewproducts.tpl');
        }
    }

    protected function getNewProducts()
    {
        $nb = (int) Configuration::get('PS_SIDEBAR_NEW_PRODUCTS_NBR', 8);
        $products = Product::getNewProducts((int) $this->context->language->id, 0, $nb);

        if (!$products) {
            return false;
        }

        $assembler = new ProductAssembler($this->context);
        $presenterFactory = new ProductPresenterFactory($this->context);
        $presentationSettings = $presenterFactory->getPresentationSettings();
        $presenter = new PrestaShop\PrestaShop\Core\Product\ProductListingPresenter(
            new PrestaShop\PrestaShop\Adapter\Image\ImageRetriever(
                $this->context->link
            ),
            $this->context->link,
            new PrestaShop\PrestaShop\Adapter\Product\PriceFormatter(),
            new PrestaShop\PrestaShop\Adapter\Product\ProductColorsRetriever(),
            $this->context->getTranslator()
        );

        $productsForTemplate = [];

        foreach ($products as $rawProduct) {
            $productsForTemplate[] = $presenter->present(
                $presentationSettings,
                $assembler->assembleProduct($rawProduct),
                $this->context->language
            );
        }

        return $productsForTemplate;
    }
}

