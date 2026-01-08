{extends file=$layout}

{block name='head' append}
  <meta property="og:type" content="product">
  {if $product.cover}
    <meta property="og:image" content="{$product.cover.large.url}">
  {/if}

  {if $product.show_price}
    <meta property="product:pretax_price:amount" content="{$product.price_tax_exc}">
    <meta property="product:pretax_price:currency" content="{$currency.iso_code}">
    <meta property="product:price:amount" content="{$product.price_amount}">
    <meta property="product:price:currency" content="{$currency.iso_code}">
  {/if}
  {if isset($product.weight) && ($product.weight != 0)}
    <meta property="product:weight:value" content="{$product.weight}">
    <meta property="product:weight:units" content="{$product.weight_unit}">
  {/if}
{/block}

{block name='head_microdata_special'}
  {include file='_partials/microdata/product-jsonld.tpl'}
{/block}

{block name='content'}

  <section id="main" class="product-details">
    <meta content="{$product.url}">

    <div class="product-details-information">
      <div class="row">
        <div class="col-md-5 col-sm-12 col-xs-12">
          {block name='page_content_container'}
            <section class="page-content" id="content">
              {block name='page_content'}
                {include file='catalog/_partials/product-flags.tpl'}

                {block name='product_cover_thumbnails'}
                  {include file='catalog/_partials/product-cover-thumbnails.tpl'}
                {/block}

                <div class="scroll-box-arrows scroll">
                  <i class="material-icons left">&#xE314;</i>
                  <i class="material-icons right">&#xE315;</i>
                </div>

              {/block}
            </section>
          {/block}
        </div>
        <div class="col-md-7 col-sm-12 col-xs-12 product-right">
          <div class="theiaStickySidebar">
            <div class="product-manufacture-logo">
              <h1 class="h1 page-title" itemprop="name">{$product.name}</h1>

              {if isset($product_manufacturer->id) && isset($manufacturer_image_url)}
                <a href="{$product_brand_url}">
                  <div class="manufacture-img">
                    <img src="{$manufacturer_image_url}" class="img img-thumbnail manufacturer-logo"
                      alt="{$product_manufacturer->name}" loading="lazy" width="98" height="50">
                  </div>
                </a>
              {/if}
            </div>

            {if isset($product.reference_to_display) && $product.reference_to_display neq ''}
              <div class="prod-id_product">ID: {$product.reference_to_display}</div>
            {/if}

            {if isset($product.ean13) && $product.ean13 neq ''}
              <div class="product-ean13">
                <label class="label">EAN13: </label>
                <span>{$product.ean13}</span>
              </div>
            {/if}

            {block name='product_prices'}
              {include file='catalog/_partials/product-prices.tpl'}
            {/block}

            {block name='product_description_short'}
              <div id="product-description-short-{$product.id}" class="product-description">
                {$product.description_short nofilter}</div>
            {/block}

            {block name='product_discounts'}
              {include file='catalog/_partials/product-discounts.tpl'}
            {/block}

            <div class="productpage-countdown"></div>

            <div class="product-information">
              {if $product.is_customizable && count($product.customizations.fields)}
                {block name='product_customization'}
                  {include file="catalog/_partials/product-customization.tpl" customizations=$product.customizations}
                {/block}
              {/if}

              <div class="product-actions js-product-actions">
                {block name='product_buy'}
                  <form action="{$urls.pages.cart}" method="post" id="add-to-cart-or-refresh">
                    <input type="hidden" name="token" value="{$static_token}">
                    <input type="hidden" name="id_product" value="{$product.id}" id="product_page_product_id">
                    <input type="hidden" name="id_customization" value="{$product.id_customization}"
                      id="product_customization_id" class="js-product-customization-id">

                    <div class="product_attributes">
                      {block name='product_variants'}
                        {include file='catalog/_partials/product-variants.tpl'}
                      {/block}
                    </div>

                    {block name='product_pack'}
                      {if $packItems}
                        <section class="product-pack">
                          <p class="h4">{l s='This pack contains' d='Shop.Theme.Catalog'}</p>
                          {foreach from=$packItems item="product_pack"}
                            {block name='product_miniature'}
                              {include file='catalog/_partials/miniatures/pack-product.tpl' product=$product_pack showPackProductsPrice=$product.show_price}
                            {/block}
                          {/foreach}
                        </section>
                      {/if}
                    {/block}

                    {block name='product_add_to_cart'}
                      {include file='catalog/_partials/product-add-to-cart.tpl'}
                    {/block}

                    {block name='product_additional_info'}
                      {include file='catalog/_partials/product-additional-info.tpl'}
                    {/block}

                    {block name='product_refresh'}{/block}
                  </form>
                {/block}
              </div>

              {block name='hook_display_reassurance'}
                {hook h='displayReassurance'}
              {/block}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="tabcontainer">
        {block name='product_tabs'}
          <div class="product-tabs tabs" role="tablist">
            <ul class="nav nav-tabs">
              {if $product.description}
                <li class="nav-item">
                  <a id="a-prod-description" data-toggle="tab" role="tab" aria-controls="description"
                    class="nav-link{if $product.description} active js-product-nav-active{/if}" href="#description"
                    aria-selected="{if $product.description}true{else}false{/if}">
                    <h2>{l s='Description' d='Shop.Theme.Catalog'}</h2>
                  </a>
                </li>
              {/if}
              {* <li class="nav-item">
                <a id="a-prod-details" role="tab" aria-controls="product-details" data-toggle="tab"
                  class="nav-link{if !$product.description} active js-product-nav-active{/if}" href="#product-details">
                  <h2>{l s='Product Details' d='Shop.Theme.Catalog'}</h2>
                </a>
              </li> *}
              {if $product.attachments}
                <li class="nav-item">
                  <a id="a-prod-attachments" role="tab" aria-controls="attachments" class="nav-link" data-toggle="tab"
                    href="#attachments">
                    {l s='Attachments' d='Shop.Theme.Catalog'}
                  </a>
                </li>
              {/if}
              {foreach from=$product.extraContent item=extra key=extraKey}
                <li class="nav-item">
                  <a id="a-prod-extra-{$extraKey}" role="tab" aria-controls="extra-{$extraKey}" class="nav-link"
                    data-toggle="tab" href="#extra-{$extraKey}">{$extra.title}</a>
                </li>
              {/foreach}
            </ul>

            <div class="tab-content" id="tab-content">
              {if $product.description}
                <div class="tab-pane fade in{if $product.description} active js-product-tab-active{/if}" id="description"
                  role="tabpanel">
                  {block name='product_description'}
                    <div class="product-description">{$product.description nofilter}</div>
                  {/block}
                </div>
              {/if}

              {block name='product_details'}
                {include file='catalog/_partials/product-details.tpl'}
              {/block}

              {block name='product_attachments'}
                {if $product.attachments}
                  <div class="tab-pane fade in" id="attachments" role="tabpanel">
                    <section class="product-attachments">
                      <p class="h5 text-uppercase">{l s='Download' d='Shop.Theme.Actions'}</p>
                      {foreach from=$product.attachments item=attachment}
                        <div class="attachment">
                          <h4><a
                              href="{url entity='attachment' params=['id_attachment' => $attachment.id_attachment]}">{$attachment.name}</a>
                          </h4>
                          <p>{$attachment.description}</p>
                          <a href="{url entity='attachment' params=['id_attachment' => $attachment.id_attachment]}">
                            {l s='Download' d='Shop.Theme.Actions'} ({$attachment.file_size_formatted})
                          </a>
                        </div>
                      {/foreach}
                    </section>
                  </div>
                {/if}
              {/block}

              {foreach from=$product.extraContent item=extra key=extraKey}
                <div class="tab-pane fade in {$extra.attr.class}" id="extra-{$extraKey}" role="tabpanel"
                  {foreach $extra.attr as $key => $val} {$key}="{$val}" {/foreach}>
                  {$extra.content nofilter}
                </div>
              {/foreach}
            </div>
          </div>
        {/block}
      </div>
    </div>

    {block name='product_accessories'}
      {if $accessories}
        <section class="product-accessories clearfix">
          <h3>Powiązane produkty</h3>
          <div id="product-accessories" class="products product-carousel owl-carousel owl-theme">
            {foreach from=$accessories item="product_accessory" key="position"}
              {block name='product_miniature'}
                {include file='catalog/_partials/miniatures/product.tpl' product=$product_accessory position=$position productClasses="col-xs-12 col-sm-6 col-lg-4 col-xl-3"}
              {/block}
            {/foreach}
          </div>
        </section>
      {/if}
    {/block}

    {block name='product_footer'}
      {* Product footer intentionally left empty *}
    {/block}

    {block name='product_images_modal'}
      {include file='catalog/_partials/product-images-modal.tpl'}
    {/block}

    {block name='page_footer_container'}
      <footer class="page-footer">
        {block name='page_footer'}
          {* Footer content intentionally left empty for product pages *}
        {/block}
      </footer>
    {/block}
  </section>

{/block}