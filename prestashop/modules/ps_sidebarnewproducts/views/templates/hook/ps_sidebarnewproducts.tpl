{**
 * Sidebar New Products
 * Displays new products in the left sidebar
 *}

{if $products}
<section id="side-new" class="block">
  <h4 class="title_block">{l s='New products' d='Shop.Theme.Catalog'}</h4>
  <div class="side-newproduct">
    {foreach from=$products item=product}
      <article class="product-miniature js-product-miniature" data-id-product="{$product.id_product}" data-id-product-attribute="{$product.id_product_attribute}">
        <div class="thumbnail-container">
          <div class="border_inside">
            <div class="product-image col-xl-4 col-lg-3 col-md-3 col-sm-3 col-xs-3">
              <a href="{$product.url}" class="thumbnail product-thumbnail">
                {if $product.cover}
                  <img
                    src="{$product.cover.bySize.small_default.url}"
                    alt="{if !empty($product.cover.legend)}{$product.cover.legend}{else}{$product.name}{/if}"
                    width="100"
                    height="100"
                    loading="lazy"
                  >
                {else}
                  <img src="{$urls.no_picture_image.bySize.small_default.url}" alt="{$product.name}" width="100" height="100" loading="lazy">
                {/if}
              </a>
            </div>
            <div class="product-description col-xl-8 col-lg-9 col-md-9 col-sm-9 col-xs-9">
              <div class="product-title">
                <a class="name" href="{$product.url}">{$product.name}</a>
              </div>
              <div class="product-price-and-shipping">
                {if $product.has_discount}
                  <span class="regular-price">{$product.regular_price}</span>
                {/if}
                <span class="price">{$product.price}</span>
              </div>
            </div>
          </div>
        </div>
      </article>
    {/foreach}
    <a href="{$allNewProductsLink}" class="btn btn-primary btn-new-prods-showall">{l s='Show all' d='Shop.Theme.Actions'}</a>
  </div>
</section>
{/if}
