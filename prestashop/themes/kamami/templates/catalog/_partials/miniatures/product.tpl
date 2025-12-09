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
{block name='product_miniature_item'}
  <article class="product-miniature thumb js-product-miniature{if !empty($productClasses)} {$productClasses}{/if}"
    data-id-product="{$product.id_product}" data-id-product-attribute="{$product.id_product_attribute}"
    {if isset($product.manufacturer_name)} data-brand="{$product.manufacturer_name}" {/if}>
    <div class="border_inside">
      <div class="thumbnail-container">
        <div class="product-image">
          {block name='product_thumbnail'}
            {if $product.cover}
              <a href="{$product.url}" class="thumbnail product-thumbnail">
                <img src="{$product.cover.bySize.home_default.url}" class="product-thumbnail-first" loading="lazy"
                  alt="{if !empty($product.cover.legend)}{$product.cover.legend}{else}{$product.name|truncate:30:'...'}{/if}"
                  data-full-size-image-url="{$product.cover.bySize.large_default.url}"
                  id="hoverproductImage_{$product.id_product}" width="{$product.cover.bySize.home_default.width}"
                  height="{$product.cover.bySize.home_default.height}" />
                {if isset($product.images) && count($product.images) > 1}
                  <div class="hover-images-toggler">
                    {foreach from=$product.images item=image}
                      <div class="image-toggle" data-hover-slider-image="{$image.bySize.home_default.url}"
                        data-hover-slider-i="{$product.id_product}-{$image.id_image}"></div>
                    {/foreach}
                  </div>
                {/if}
              </a>
            {else}
              <a href="{$product.url}" class="thumbnail product-thumbnail">
                <img src="{$urls.no_picture_image.bySize.home_default.url}" class="product-thumbnail-first" loading="lazy"
                  width="{$urls.no_picture_image.bySize.home_default.width}"
                  height="{$urls.no_picture_image.bySize.home_default.height}" />
              </a>
            {/if}
          {/block}

          <div class="cartbottom_btn btn_hover">
            {block name='quick_view'}
              <div class="quick-view-wrapper">
                <a class="quick-view" href="#" data-link-action="quickview" aria-label="{$product.name}">
                  <i class="redfox-preview"></i>
                </a>
              </div>
            {/block}

            {block name='product_compare'}
              {hook h='displayProductCompareButton' product=$product}
            {/block}
          </div>

          {block name='product_flags'}
            <ul class="product-flags">
              {foreach from=$product.flags item=flag}
                <li class="product-flag {$flag.type}"><span>{$flag.label}</span></li>
              {/foreach}
            </ul>
          {/block}
        </div>
      </div>

      <div class="product_desc">
        <div class="product-description">
          {block name='product_name'}
            <div class="product-title" itemprop="name">
              <a href="{$product.url}" class="name">{$product.name}</a>
            </div>
          {/block}

          {block name='product_description_short'}
            {if isset($product.description_short) && $product.description_short}
              <div class="description_short">{$product.description_short nofilter}</div>
            {/if}
          {/block}

          <div class="desc-block">
            <div class="desc-left">
              {block name='product_price_and_shipping'}
                {if $product.show_price}
                  <div class="product-price-and-shipping">
                    {if $product.has_discount}
                      <span class="sr-only">{l s='Regular price' d='Shop.Theme.Catalog'}</span>
                      <span class="regular-price">{$product.regular_price}</span>
                    {/if}
                    <span itemprop="price" class="price{if $product.has_discount} discount-price{/if}">{$product.price}</span>
                  </div>
                {/if}
              {/block}

              {block name='product_delivery_time'}
                <div class="delivery-time">
                  {if isset($product.availability_message) && $product.availability_message}
                    <i
                      class="material-icons {if $product.availability === 'available'}product-available{else}product-unavailable{/if}">&#xE8B6;</i>
                    {$product.availability_message}
                  {/if}
                  {if isset($product.quantity) && $product.quantity > 0}
                    <div class="avail_quantity">
                      {l s='Available quantity:' d='Shop.Theme.Catalog'} {$product.quantity}
                    </div>
                  {/if}
                </div>
              {/block}
            </div>

            <div class="desc-right">
              {block name='product_add_to_cart'}
                {if !$configuration.is_catalog}
                  <form action="{$urls.pages.cart}" method="post" class="add-to-cart-or-refresh">
                    <input type="hidden" name="id_product" value="{$product.id_product}">
                    <input type="hidden" name="qty" value="1" min="1">
                    <input type="hidden" name="id_product_attribute" value="{$product.id_product_attribute}">
                    <input type="hidden" name="token" value="{$static_token}">
                    <button class="btn btn-primary add-to-cart no-added" data-button-action="add-to-cart" type="submit"
                      aria-label="{l s='Add to cart' d='Shop.Theme.Actions'}">
                      <div class="addcart_ico">
                        <span class="redfox-cart"></span>
                        <span class="redfox-checkmark"></span>
                        <span class="redfox-loading"></span>
                      </div>
                    </button>
                  </form>
                {/if}
              {/block}
            </div>
          </div>
        </div>

        <div class="info-inner">
          <div class="stock-count">
            {if isset($product.quantity) && $product.quantity > 0}
              <div class="stock-available-countdown" quantity-max="{$product.quantity}">
                <div class="product-availability">
                  <i class="material-icons rtl-no-flip product-available">&#xE8B6;</i>
                  {if $product.availability === 'available'}
                    {l s='Available' d='Shop.Theme.Catalog'}
                  {else}
                    {l s='Out of stock' d='Shop.Theme.Catalog'}
                  {/if}
                </div>
              </div>
            {/if}
          </div>
        </div>
      </div>
    </div>
  </article>
{/block}