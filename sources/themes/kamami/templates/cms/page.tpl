{extends file='page.tpl'}

{block name='page_title'}
  {$cms.meta_title}
{/block}

{block name='content'}
  <section id="main">
    {block name='page_header_container'}
      <header class="page-header">
        <h1>
          {$cms.meta_title}
        </h1>
      </header>
    {/block}

    {block name='page_content_container'}
      <section id="content" class="page-content page-cms page-cms-{$cms.id}">
        {block name='cms_content'}
          {$cms.content nofilter}
        {/block}

        {block name='hook_cms_dispute_information'}
          {hook h='displayCMSDisputeInformation'}
        {/block}

        {block name='hook_cms_print_button'}
          {hook h='displayCMSPrintButton'}
        {/block}
      </section>
    {/block}
  </section>
{/block}