{extends file='parent:_partials/header.tpl'}

{block name='header_nav'}
  <nav class="header-nav">
    <div class="container d-flex align-items-center">
      <div class="col-lg-7 col-md-7 col-xs-12 left-nav">
        {hook h='displayNav1'}
      </div>
      <div class="col-lg-5 col-md-5 right-nav hidden-sm-down">
        <div id="_desktop_contact_link">
          <div id="contact-link" class="ajax-contactinfo-src">
            <a href="{$urls.pages.contact}">
              <i class="redfox-message"></i>
              <span class="hidden-sm-down">{l s='Contact us' d='Shop.Theme.Global'}</span>
            </a>
          </div>
        </div>
        {hook h='displayNav2'}
      </div>
    </div>
  </nav>
{/block}

{block name='header_top'}
  <div id="header_part" class="main-header-container">
    <div class="main-header">
      <div class="main-header-logo">
        {renderLogo}
      </div>
      <div class="main-header-break"></div>
      {hook h='displaySearch'}
      <div class="main-header-rest">
        {hook h='displayTop'}
        <div id="_desktop_wishtlistTop" class="pull-right">
          <div class="wishtlistTop ajax-wishlist-src">
            <a class="wishtlist_top" href="{$link->getModuleLink('blockwishlist', 'lists')}"
              title="{l s='My wishlists' d='Shop.Theme.Global'}">
              <i class="redfox-heart"></i>
              <span class="nb-count wishlist-nb">0</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
  {hook h='displayNavFullWidth'}
{/block}