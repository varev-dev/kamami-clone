<div class="product-add-to-cart js-product-add-to-cart">
  {if !$configuration.is_catalog}
    {if $product.is_virtual == 0}
      <div class="delivery-prod">
        {if $product.quantity > 0}
          {if $product.additional_delivery_times == 2 && $product.delivery_in_stock}
            <i class="material-icons product-available">local_shipping</i> {$product.delivery_in_stock}
          {else}
            <i class="material-icons product-unavailable">local_shipping</i> 24h
          {/if}
        {else}
          <i class="material-icons product-unavailable">local_shipping</i> 24h
        {/if}
      </div>
    {/if}

    {block name='product_availability'}
      <span id="product-availability" class="js-product-availability">
        {if $product.show_availability && $product.availability_message}
          {if $product.availability == 'available'}
            <i class="material-icons rtl-no-flip product-available">&#xE5CA;</i>
          {elseif $product.availability == 'last_remaining_items'}
            <i class="material-icons product-last-items">&#xE002;</i>
          {else}
            <i class="material-icons product-unavailable">&#xE14B;</i>
          {/if}
          {$product.availability_message}
        {/if}
      </span>
    {/block}

    {if $product.show_quantities && $product.quantity > 0}
      <div class="product-stock-k">
        <div class="product-stock-k-dlg" id="product-stock-k-dlg-{$product.id}">
          {l s='Available quantity:' d='Shop.Theme.Catalog'}
          {$product.quantity}
        </div>
      </div>
    {/if}

    <div class="add-to-cart-wrapper">
      {block name='product_quantity'}
        <div class="product-quantity clearfix">
          <div class="qty">
            <div class="input-group bootstrap-touchspin">
              <span class="input-group-addon bootstrap-touchspin-prefix" style="display: none;"></span>
              <input type="text" name="qty" id="quantity_wanted" inputmode="numeric" pattern="[0-9]*"
                {if $product.quantity_wanted} value="{$product.quantity_wanted}" min="{$product.minimal_quantity}" 
                {else}
                value="1" min="1" {/if} class="input-group form-control"
                aria-label="{l s='Quantity' d='Shop.Theme.Actions'}" style="display: block;">
              <span class="input-group-addon bootstrap-touchspin-postfix" style="display: none;"></span>
              <span class="input-group-btn-vertical">
                <button class="btn btn-touchspin js-touchspin bootstrap-touchspin-up" type="button" aria-label="+">
                  <i class="material-icons touchspin-up"></i>
                </button>
                <button class="btn btn-touchspin js-touchspin bootstrap-touchspin-down" type="button" aria-label="-">
                  <i class="material-icons touchspin-down"></i>
                </button>
              </span>
            </div>
          </div>
          <div class="add">
            <button class="btn btn-primary add-to-cart no-added" data-button-action="add-to-cart" type="submit"
              data-id-product="{$product.id}" {if !$product.add_to_cart_url} disabled {/if}>
              <div class="addcart_ico">
                <span class="redfox-cart"></span>
                <span class="redfox-checkmark"></span>
                <span class="redfox-loading"></span>
              </div>
              <div class="addcart_text">{l s='Add to cart' d='Shop.Theme.Actions'}</div>
            </button>
          </div>

          <div class="product-additional-button">
            {hook h='displayProductActions' product=$product}
          </div>
        </div>
      {/block}
    </div>

    {block name='product_minimal_quantity'}
      <p class="product-minimal-quantity js-product-minimal-quantity">
        {if $product.minimal_quantity > 1}
          {l
                                                                s='The minimum purchase order quantity for the product is %quantity%.'
                                                                d='Shop.Theme.Checkout'
                                                                sprintf=['%quantity%' => $product.minimal_quantity]
                                                                }
        {/if}
      </p>
    {/block}
  {/if}
</div>