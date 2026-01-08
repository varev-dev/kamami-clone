<div id="_desktop_cart" class="pull-right">
  <div class="blockcart cart-preview {if $cart.products_count > 0}active{else}inactive{/if}"
    data-refresh-url="{$refresh_url}">
    <div class="header shopping_cart">
      <div class="totalprice" title="{l s='Cart' d='Shop.Theme.Checkout'}">
        <a rel="nofollow" class="js-cart-modal-trigger"
          aria-label="{l s='Shopping cart link containing %nbProducts% product(s)' sprintf=['%nbProducts%' => $cart.products_count] d='Shop.Theme.Checkout'}"
          href="#">
          <i class="redfox-shopping-bag" aria-hidden="true"></i>
          <span class="cart-products-count price_circle hidden-md-up">{$cart.products_count}</span>
          <div class="cartshop hidden-sm-down">
            <span class="cart-products-count price_circle">{$cart.products_count}</span>
            <span class="cart-empty hide-source">{$cart.subtotals.products.value}</span>
          </div>
        </a>
      </div>
    </div>
  </div>
</div>

{* Include cart modal - PrestaShop renders modal.tpl dynamically, but we need it in DOM for manual opening *}
{include file='module:ps_shoppingcart/modal.tpl'}