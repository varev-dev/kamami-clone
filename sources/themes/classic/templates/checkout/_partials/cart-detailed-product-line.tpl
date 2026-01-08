{**
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
 *}
<div class="fcart-item">
  <!-- Column 1: Number -->
  <div>{if isset($index)}{$index + 1}{else}1{/if}</div>

  <!-- Column 2: Image -->
  <div>
    {if $product.default_image}
      <img src="{$product.default_image.bySize.cart_default.url}" alt="{$product.name|escape:'quotes'}" loading="lazy">
    {else}
      <img src="{$urls.no_picture_image.bySize.cart_default.url}" alt="{$product.name|escape:'quotes'}" loading="lazy">
    {/if}
  </div>

  <!-- Column 3: Product Name -->
  <div>
    <a class="label" href="{$product.url}"
      data-id_customization="{$product.id_customization|intval}">{$product.name}</a>
    {foreach from=$product.attributes key="attribute" item="value"}
      <div class="product-line-info {$attribute|lower}">
        <span class="label">{$attribute}:</span>
        <span class="value">{$value}</span>
      </div>
    {/foreach}
    {if is_array($product.customizations) && $product.customizations|count}
      {block name='cart_detailed_product_line_customization'}
        {foreach from=$product.customizations item="customization"}
          <a href="#" data-toggle="modal"
            data-target="#product-customizations-modal-{$customization.id_customization}">{l s='Product customization' d='Shop.Theme.Catalog'}</a>
          <div class="modal fade customization-modal" id="product-customizations-modal-{$customization.id_customization}"
            tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal" aria-label="{l s='Close' d='Shop.Theme.Global'}">
                    <span aria-hidden="true">&times;</span>
                  </button>
                  <h4 class="modal-title">{l s='Product customization' d='Shop.Theme.Catalog'}</h4>
                </div>
                <div class="modal-body">
                  {foreach from=$customization.fields item="field"}
                    <div class="product-customization-line row">
                      <div class="col-sm-3 col-xs-4 label">
                        {$field.label}
                      </div>
                      <div class="col-sm-9 col-xs-8 value">
                        {if $field.type == 'text'}
                          {if (int)$field.id_module}
                            {$field.text nofilter}
                          {else}
                            {$field.text}
                          {/if}
                        {elseif $field.type == 'image'}
                          <img src="{$field.image.small.url}" loading="lazy">
                        {/if}
                      </div>
                    </div>
                  {/foreach}
                </div>
              </div>
            </div>
          </div>
        {/foreach}
      {/block}
    {/if}
  </div>

  <!-- Column 4: Availability -->
  <div>
    {if isset($product.availability) && $product.availability == 'available'}
      <div class="cart_in_stock_prod_l1">{l s='Available' d='Shop.Theme.Checkout'}</div>
    {elseif isset($product.availability) && $product.availability == 'last_remaining_items'}
      <div class="cart_in_stock_prod_l1">{l s='Last items in stock' d='Shop.Theme.Checkout'}</div>
    {elseif isset($product.availability) && $product.availability == 'unavailable'}
      <div class="cart_out_of_stock_prod">
        <div class="cart_out_of_stock_prod_l1">Brak w magazynie</div>
      </div>
    {else}
      <div class="cart_in_stock_prod_l1">{l s='Available' d='Shop.Theme.Checkout'}</div>
    {/if}
  </div>

  <!-- Column 5: Price (tax incl.) -->
  <div>
    <div class="product-price">
      {if $product.unit_price_full}
        <div class="unit-price-cart">{$product.unit_price_full}</div>
      {else}
        <div class="unit-price-cart">{$product.price}</div>
      {/if}
    </div>
  </div>

  <!-- Column 6: Quantity -->
  <div>
    {if !empty($product.is_gift)}
      <div class="input-group bootstrap-touchspin">
        <span class="input-group-addon bootstrap-touchspin-prefix" style="display: none;"></span>
        <input class="form-control" type="text" value="{$product.quantity}" disabled>
        <span class="input-group-addon bootstrap-touchspin-postfix" style="display: none;"></span>
      </div>
    {else}
      <div class="input-group bootstrap-touchspin">
        <span class="input-group-addon bootstrap-touchspin-prefix" style="display: none;"></span>
        <input class="js-cart-line-product-quantity form-control" data-down-url="{$product.down_quantity_url}"
          data-up-url="{$product.up_quantity_url}" data-update-url="{$product.update_quantity_url}"
          data-product-id="{$product.id_product}" type="text" inputmode="numeric" pattern="[0-9]*"
          value="{$product.quantity}" name="product-quantity-spin"
          aria-label="{l s='%productName% product quantity field' sprintf=['%productName%' => $product.name] d='Shop.Theme.Checkout'}">
        <span class="input-group-addon bootstrap-touchspin-postfix" style="display: none;"></span>
        <span class="input-group-btn-vertical">
          <button class="btn btn-touchspin js-touchspin js-increase-product-quantity bootstrap-touchspin-up" type="button"
            aria-label="+">
            <i class="material-icons touchspin-up">keyboard_arrow_up</i>
          </button>
          <button class="btn btn-touchspin js-touchspin js-decrease-product-quantity bootstrap-touchspin-down"
            type="button" aria-label="-">
            <i class="material-icons touchspin-down">keyboard_arrow_down</i>
          </button>
        </span>
      </div>
    {/if}
  </div>

  <!-- Column 7: Total (tax incl.) -->
  <div>
    {if !empty($product.is_gift)}
      <span class="gift">{l s='Gift' d='Shop.Theme.Checkout'}</span>
    {else}
      <span class="total-amnt">{$product.total}</span>
    {/if}
  </div>

  <!-- Column 8: Actions (Delete) -->
  <div>
    <div class="cart-line-product-actions">
      <a class="remove-from-cart" rel="nofollow" href="{$product.remove_from_cart_url}"
        data-link-action="delete-from-cart" data-id-product="{$product.id_product|escape:'javascript'}"
        data-id-product-attribute="{$product.id_product_attribute|escape:'javascript'}"
        data-id-customization="{$product.id_customization|escape:'javascript'}">
        {if empty($product.is_gift)}
          <i class="material-icons float-xs-left">delete</i>
        {/if}
      </a>
      {block name='hook_cart_extra_product_actions'}
        {hook h='displayCartExtraProductActions' product=$product}
      {/block}
    </div>
  </div>

  <!-- Mobile price total (hidden on desktop) -->
  <div class="mobile-price-total">
    <div class="price">
      {l s='Price (tax incl.)' d='Shop.Theme.Checkout'}
      {if $product.unit_price_full}
        <div class="unit-price-cart">{$product.unit_price_full}</div>
      {else}
        <div class="unit-price-cart">{$product.price}</div>
      {/if}
    </div>
    <div class="total">
      {l s='Total (tax incl.)' d='Shop.Theme.Checkout'}
      <span class="total-amnt">
        {if !empty($product.is_gift)}
          <span class="gift">{l s='Gift' d='Shop.Theme.Checkout'}</span>
        {else}
          {$product.total}
        {/if}
      </span>
    </div>
  </div>
</div>