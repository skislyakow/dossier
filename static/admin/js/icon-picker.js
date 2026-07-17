var ICON_CATEGORIES = [
  {name: 'Programming', icons: ['code', 'code_off', 'data_object', 'data_array', 'functions', 'terminal', 'database', 'storage', 'cloud', 'dns', 'api', 'menu_book', 'school', 'auto_awesome', 'smart_toy', 'integration_instructions']},
  {name: 'DevOps', icons: ['settings', 'build', 'construction', 'deployed_code', 'deployed_code_update', 'deployed_code_history', 'network_node', 'cloud_sync', 'cloud_done', 'cloud_queue']},
  {name: 'Tools', icons: ['bug_report', 'account_tree', 'account_balance', 'schema', 'science', 'biotech', 'psychology', 'neurology', 'troubleshoot', 'frame_source', 'manage_search', 'search', 'tune', 'filter_alt', 'sort']},
  {name: 'Git', icons: ['commit', 'branch', 'merge', 'fork_left', 'fork_right', 'call_split', 'call_merge', 'compare_arrows', 'update', 'downloading']},
  {name: 'Data', icons: ['dataset', 'dataset_linked', 'table', 'table_rows', 'database', 'bar_chart', 'pie_chart', 'trending_up', 'trending_down', 'monitoring', 'analytics', 'insights', 'data_exploration', 'cognition']},
  {name: 'Communication', icons: ['mail', 'send', 'chat', 'sms', 'call', 'link', 'hub', 'notifications', 'campaign', 'rss_feed']},
  {name: 'Web', icons: ['public', 'language', 'web', 'webhook', 'http', 'globe', 'travel_explore', 'explore', 'new_window', 'iframe', 'publish']},
  {name: 'Design', icons: ['palette', 'colorize', 'design_services', 'draw', 'brush', 'style', 'text_fields', 'format_bold', 'format_italic', 'auto_fix', 'magic']},
  {name: 'UI', icons: ['dashboard', 'widgets', 'view_quilt', 'view_module', 'view_carousel', 'grid_view', 'list', 'table', 'timeline', 'calendar_month', 'schedule', 'history', 'star', 'favorite', 'thumb_up', 'check_circle', 'info', 'warning', 'error', 'help']},
  {name: 'Hardware', icons: ['computer', 'laptop', 'phone_android', 'smartphone', 'memory', 'developer_board', 'cable', 'power', 'battery_charging_full', 'sensors']},
];

document.addEventListener('alpine:init', function() {
  Alpine.data('iconPicker', function(initial) {
    return {
      icon: initial || '',
      open: false,
      query: '',
      filteredCategories: ICON_CATEGORIES,

      init: function() {
        var self = this;
        this.$watch('query', function(val) {
          self.filterCategories(val);
        });
        this.filterCategories('');
      },

      filterCategories: function(q) {
        var self = this;
        if (!q) {
          this.filteredCategories = ICON_CATEGORIES;
          return;
        }
        var lower = q.toLowerCase();
        this.filteredCategories = ICON_CATEGORIES.map(function(cat) {
          var matching = cat.icons.filter(function(i) { return i.indexOf(lower) !== -1; });
          if (matching.length === 0) return null;
          return {name: cat.name, icons: matching};
        }).filter(function(c) { return c !== null; });
      },

      onInput: function(ev) {
        this.icon = ev.target.value;
      },

      onQuery: function(ev) {
        this.query = ev.target.value;
      },

      select: function(name) {
        this.icon = name;
        this.open = false;
        this.query = '';
      },

      clear: function() {
        this.icon = '';
        this.open = false;
        this.query = '';
      },
    };
  });
});
