{**
 * Sidebar New Products Block
 * Displays new products in a compact sidebar format
 *}
<section id="side-new" class="block">
  <h4 class="title_block">{l s='Nowości' d='Modules.Sidebarnewproducts.Shop'}</h4>

  <div class="side-newproduct">
    {foreach from=$products item="product"}
      <article class="product-miniature js-product-miniature side-newproduct-item" data-id-product="{$product.id_product}"
        data-id-product-attribute="{$product.id_product_attribute}">
        <div class="thumbnail-container">
          <div class="border_inside">
            <div class="product-image col-xl-4 col-lg-3 col-md-3 col-sm-3 col-xs-3">
              <a href="{$product.url}" class="thumbnail product-thumbnail">
                {if $product.cover}
                  <img src="{$product.cover.bySize.small_default.url}"
                    alt="{if !empty($product.cover.legend)}{$product.cover.legend}{else}{$product.name|truncate:30:'...'}{/if}"
                    width="100" height="100">
                {else}
                  <img src="{$urls.no_picture_image.bySize.small_default.url}" alt="{$product.name|truncate:30:'...'}"
                    width="100" height="100">
                {/if}
              </a>
            </div>

            <div class="product-description col-xl-8 col-lg-9 col-md-9 col-sm-9 col-xs-9">
              <div class="product-title">
                <a class="name" href="{$product.url}">{$product.name}</a>
              </div>

              <div class="product-price-and-shipping">
                <span class="price">{$product.price}</span>
              </div>
            </div>
          </div>
        </div>
      </article>
    {/foreach}

    <a href="{$allNewProductsLink}" class="btn btn-primary btn-new-prods-showall">
      {l s='Pokaż wszystkie' d='Modules.Sidebarnewproducts.Shop'}
    </a>
  </div>
</section>