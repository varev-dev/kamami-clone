{* Custom Cart Modal - Replaces default PrestaShop Bootstrap modal with side panel *}
<div class="cart_block_ajax">
  <div class="cartclosebtn">
    <i class="material-icons close">close</i>
  </div>
  <div id="blockcart-sideview" class="cart-dropdown js-cart-duplicate" data-refresh-url="{$refresh_url}">
    <div class="cart-wrap">
      <div class="cart-header">
        <div class="js_cart_title">Koszyk</div>
      </div>
      <div class="block_content">
        <div class="cart_block_list">
          <ul class="products">
            {if $cart.products_count > 0}
              {foreach from=$cart.products item=product}
                <li class="first_item">
                  <span class="product-quantity">{$product.quantity}<span>&nbsp;x&nbsp;</span></span>
                  <a class="cart-images" href="{$product.url}">
                    {if $product.default_image}
                      <img width="45" height="45" src="{$product.default_image.bySize.cart_default.url}"
                        alt="{$product.name|escape:'html':'UTF-8'}" loading="lazy">
                    {else}
                      <img width="45" height="45" src="{$urls.no_picture_image.bySize.cart_default.url}"
                        alt="{$product.name|escape:'html':'UTF-8'}" loading="lazy">
                    {/if}
                  </a>
                  <div class="cart-info">
                    <div class="product-name">{$product.name}</div>
                    <span class="price">{$product.price}</span>
                    <div class="cart-product-info"></div>
                  </div>
                  <span class="remove_link">
                    <a class="remove-from-cart" rel="nofollow" href="{$product.remove_from_cart_url}"
                      data-link-action="delete-from-cart" data-id-product="{$product.id_product}"
                      data-id-product-attribute="{$product.id_product_attribute}" data-id-customization=""
                      title="usuń z koszyka"></a>
                  </span>
                </li>
              {/foreach}
            {else}
              <div class="no-product-label">Brak produktów w koszyku</div>
            {/if}
          </ul>
          {if $cart.products_count > 0}
            <div class="cart-detailed-totals">
              <p class="cart-products-count">Ilość produktów w Twoim koszyku: {$cart.products_count}.</p>
              <div class="card-block">
                <div class="cart-summary-line products">
                  <span class="label">Produkty</span>
                  <span class="value price">{$cart.subtotals.products.value}</span>
                </div>
                {if $cart.subtotals.shipping.value}
                  <div class="cart-summary-line shipping">
                    <span class="label">Wysyłka</span>
                    <span class="value price">{$cart.subtotals.shipping.value}</span>
                  </div>
                {else}
                  <div class="cart-summary-line shipping">
                    <span class="label">Wysyłka</span>
                    <span class="value price">Za darmo!</span>
                  </div>
                {/if}
              </div>
              <hr>
              <div class="cart-summary-totals">
                <div class="cart-summary-line cart-total">
                  <span class="label">Razem</span>
                  <span class="value price">{$cart.totals.total.value}</span>
                </div>
              </div>
            </div>
            <div class="cartmodal-btn">
              <a class="btn btn-primary text-uppercase" href="{$cart_url}">Realizuj zamówienie</a>
            </div>
          {/if}
        </div>
      </div>
    </div>
  </div>
</div>
<div class="cart-overlayer"></div>

<style type="text/css">
  #blockcart-modal {
    display: none !important;
    visibility: hidden !important;
  }

  .cart_block_list .first_item {
    position: relative;
    overflow: visible;
  }

  .cart_block_ajax .remove_link {
    position: absolute;
    right: 0;
    top: 10px;
  }

  .cart_block_ajax .remove-from-cart {
    display: block;
    width: auto;
    height: auto;
    padding: 0;
  }
</style>