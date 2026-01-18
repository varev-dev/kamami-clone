{extends file='page.tpl'}

{block name='page_header_container'}{/block}

{if $layout === 'layouts/layout-left-column.tpl'}
  {block name="left_column"}
    <div id="left-column" class="col-xs-12 col-sm-12 col-md-3 sidebar"
      style="position: relative; overflow: visible; box-sizing: border-box; min-height: 1px;">
      <div class="theiaStickySidebar" style="padding-top: 0px; padding-bottom: 1px; position: static; transform: none;">
        {widget name="ps_contactinfo" hook='displayLeftColumn'}
      </div>
    </div>
  {/block}
{else if $layout === 'layouts/layout-right-column.tpl'}
  {block name="right_column"}
    <div id="right-column" class="col-xs-12 col-sm-12 col-md-3 sidebar"
      style="position: relative; overflow: visible; box-sizing: border-box; min-height: 1px;">
      <div class="theiaStickySidebar" style="padding-top: 0px; padding-bottom: 1px; position: static; transform: none;">
        {widget name="ps_contactinfo" hook='displayRightColumn'}
      </div>
    </div>
  {/block}
{/if}

{block name="content_wrapper"}
  <div id="content-wrapper" class="left-column col-xs-12 col-sm-12 col-md-12 col-lg-12 col-xl-9 withsidebar"
    style="position: relative; overflow: visible; box-sizing: border-box; min-height: 1px;">
    <div class="theiaStickySidebar" style="padding-top: 0px; padding-bottom: 1px; position: static; transform: none;">
      {block name='page_content'}
        <section id="main">
          <section id="content" class="page-content card card-block">
            {widget name="contactform"}
          </section>
        </section>
      {/block}
    </div>
  </div>
{/block}