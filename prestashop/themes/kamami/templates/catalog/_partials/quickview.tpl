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
<div id="quickview-modal-{$product.id}-{$product.id_product_attribute}" class="modal fade quickview" tabindex="-1"
  role="dialog" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="{l s='Close' d='Shop.Theme.Global'}">
          <span aria-hidden="true">×</span>
        </button>
      </div>
      <div class="modal-body">
        <div class="row">
          <div class="col-md-6 col-sm-6 hidden-xs-down">
            {block name='product_cover_thumbnails'}
              <div class="images-container js-images-container">
                <div class="product-cover">
                  {if $product.cover}
                    <img class="js-qv-product-cover img-fluid" src="{$product.cover.bySize.large_default.url}"
                      alt="{$product.cover.legend}" width="{$product.cover.bySize.large_default.width}"
                      height="{$product.cover.bySize.large_default.height}">
                  {else}
                    <img class="js-qv-product-cover img-fluid" src="{$urls.no_picture_image.bySize.large_default.url}"
                      alt="{$product.name}" width="{$urls.no_picture_image.bySize.large_default.width}"
                      height="{$urls.no_picture_image.bySize.large_default.height}">
                  {/if}
                  <div class="layer hidden-sm-down" data-toggle="modal" data-target="#product-modal">
                    <i class="material-icons zoom-in">search</i>
                  </div>
                </div>

                {if isset($product.images) && count($product.images) > 1}
                  <div class="js-qv-mask mask">
                    <ul class="product-images js-qv-product-images">
                      {foreach from=$product.images item=image}
                        <li class="thumb-container js-thumb-container">
                          <img
                            class="thumb js-thumb{if $image.id_image == $product.cover.id_image} selected js-thumb-selected{/if}"
                            data-image-medium-src="{$image.bySize.medium_default.url}"
                            data-image-large-src="{$image.bySize.large_default.url}" src="{$image.bySize.small_default.url}"
                            alt="{$image.legend}" loading="lazy" width="100" height="100">
                        </li>
                      {/foreach}
                    </ul>
                  </div>
                {/if}
              </div>
            {/block}
            <div class="arrows js-arrows" style="display: none;">
              <i class="material-icons arrow-up js-arrow-up">&#xE316;</i>
              <i class="material-icons arrow-down js-arrow-down">&#xE313;</i>
            </div>
          </div>
          <div class="col-md-6 col-sm-6">
            <div class="product-manufacture-logo">
              {if isset($product.manufacturer_name) && $product.manufacturer_name}
                <a href="{$product.manufacturer_url}">
                  <h1 class="h1 page-title">{$product.name}</h1>
                </a>
              {else}
                <h1 class="h1 page-title">{$product.name}</h1>
              {/if}
            </div>

            {block name='product_prices'}
              <div class="product-prices js-product-prices">
                <div class="product-price h5">
                  <div class="current-price">
                    <span class="current-price-value" content="{$product.price_amount}">
                      {$product.price}
                    </span>
                  </div>
                  {if $product.has_discount}
                    <span class="sr-only">{l s='Regular price' d='Shop.Theme.Catalog'}</span>
                    <span class="regular-price">{$product.regular_price}</span>
                  {/if}
                </div>
                <div class="tax-shipping-delivery-label">
                  {if $configuration.display_taxes_label}
                    {l s='Tax included' d='Shop.Theme.Catalog'}
                  {else}
                    {l s='Tax excluded' d='Shop.Theme.Catalog'}
                  {/if}
                </div>
                {if $product.has_discount && $product.discount_type === 'percentage'}
                  <p class="product-without-taxes">{$product.regular_price} {l s='Netto' d='Shop.Theme.Catalog'}</p>
                {/if}
              </div>
            {/block}

            {block name='product_description_short'}
              {if $product.description_short}
                <div class="product-description">
                  <p>{$product.description_short nofilter}</p>
                </div>
              {/if}
            {/block}

            {block name='product_buy'}
              <div class="product-actions js-product-actions">
                <form action="{$urls.pages.cart}" method="post" id="add-to-cart-or-refresh">
                  <input type="hidden" name="token" value="{$static_token}">
                  <input type="hidden" name="id_product" value="{$product.id}" id="product_page_product_id">
                  <input type="hidden" name="id_customization" value="0" id="product_customization_id"
                    class="js-product-customization-id">

                  {block name='product_variants'}
                    {if isset($product.main_variants) && $product.main_variants}
                      <div class="product-variants js-product-variants">
                        {include file='catalog/_partials/variant-links.tpl' variants=$product.main_variants}
                      </div>
                    {/if}
                  {/block}

                  <div class="qv-product-id">ID: {$product.id}</div>

                  <div class="product-add-to-cart js-product-add-to-cart">
                    <span id="product-availability" class="js-product-availability">
                      <i
                        class="material-icons rtl-no-flip {if $product.availability === 'available'}product-available{else}product-unavailable{/if}">&#xE8B6;</i>
                      {if $product.availability === 'available'}
                        {l s='Available' d='Shop.Theme.Catalog'}
                      {else}
                        {l s='Out of stock' d='Shop.Theme.Catalog'}
                      {/if}
                    </span>

                    {if isset($product.quantity) && $product.quantity > 0}
                      <div class="product-stock-k">
                        <div class="product-stock-k-dlg" id="product-stock-k-dlg-{$product.id}">
                          {l s='Available quantity:' d='Shop.Theme.Catalog'}
                          {$product.quantity}
                        </div>
                      </div>
                    {/if}

                    <div class="add-to-cart-wrapper">
                      {if !$configuration.is_catalog}
                        <div class="product-quantity clearfix">
                          <div class="qty">
                            <div class="input-group bootstrap-touchspin">
                              <input type="text" name="qty" id="quantity_wanted" inputmode="numeric" pattern="[0-9]*"
                                value="1" min="1" class="input-group form-control"
                                aria-label="{l s='Quantity' d='Shop.Theme.Catalog'}" style="display: block;">
                              <span class="input-group-btn-vertical">
                                <button class="btn btn-touchspin js-touchspin bootstrap-touchspin-up" type="button">
                                  <i class="material-icons touchspin-up"></i>
                                </button>
                                <button class="btn btn-touchspin js-touchspin bootstrap-touchspin-down" type="button">
                                  <i class="material-icons touchspin-down"></i>
                                </button>
                              </span>
                            </div>
                          </div>
                          <div class="add">
                            <button class="btn btn-primary add-to-cart no-added" data-button-action="add-to-cart"
                              type="submit" data-id-product="{$product.id}">
                              <div class="addcart_ico">
                                <span class="redfox-cart"></span>
                                <span class="redfox-checkmark"></span>
                                <span class="redfox-loading"></span>
                              </div>
                              <div class="addcart_text">{l s='Add to cart' d='Shop.Theme.Actions'}</div>
                            </button>
                          </div>
                          <div class="product-additional-button">
                            {block name='product_wishlist'}
                              <a id="wishlist_button" href="#" class="btn btn-primary wishlist-button"
                                data-product-id="{$product.id}" data-product-attribute-id="{$product.id_product_attribute}"
                                rel="nofollow" title="{l s='Add to Wishlist' d='Shop.Theme.Actions'}"
                                aria-label="{l s='Add to Wishlist' d='Shop.Theme.Actions'}">
                                <div class="wishlist-icon"><i class="redfox-heart"></i></div>
                              </a>
                            {/block}

                            {block name='product_compare'}
                              {hook h='displayProductCompareButton' product=$product}
                            {/block}
                          </div>
                        </div>
                      {/if}
                    </div>
                  </div>
                </form>
              </div>
            {/block}
          </div>
        </div>
      </div>
    </div>
  </div>
</div>