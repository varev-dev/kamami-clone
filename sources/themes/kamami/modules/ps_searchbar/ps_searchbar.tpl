<div class="main-header-search">
  <div id="_mobile_catmenu" class="hidden-xl-up pull-left">
    <div class="cat-menu-trigger">
      <i class="redfox-menu"></i>
      <span class="cat-menu-label">Menu</span>
    </div>
  </div>
  <div class="main-header-search-spacer"></div>
  <div class="jss-ctrl-wrap">
    <form action="{$search_controller_url}" method="GET" id="jss-search-form" autocomplete="off">
      <input type="hidden" name="controller" value="search">
      <input type="text" id="jss-search-input-text" name="s" value="{$search_string}"
        aria-label="{l s='Search our catalog' d='Shop.Theme.Catalog'}" autocomplete="off">
      <button id="jss-search-btn" aria-label="{l s='Search' d='Shop.Theme.Catalog'}">
        <i class="material-icons search" aria-hidden="true"></i>
      </button>
    </form>
  </div>
</div>