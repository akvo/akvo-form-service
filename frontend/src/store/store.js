import { Store } from "pullstate";

const defGlobalStore = {
  loading: false,
  forms: [],
};

const GlobalStore = new Store({
  ...defGlobalStore,
});

export default GlobalStore;
