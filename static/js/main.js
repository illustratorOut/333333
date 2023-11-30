import { Autocomplete, Collapse, Dropdown, Input, Ripple, initMDB } from "mdb-ui-kit";

initMDB({ Collapse, Dropdown, Input, Ripple });

const navbarAutocomplete = document.querySelector('#navbar-search-autocomplete');
const navbarData = ['One', 'Two', 'Three', 'Four', 'Five'];
const navbarDataFilter = (value) => {
  return navbarData.filter((item) => {
    return item.toLowerCase().startsWith(value.toLowerCase());
  });
};

new Autocomplete(navbarAutocomplete, {
  filter: navbarDataFilter,
});