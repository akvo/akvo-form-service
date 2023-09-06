import { Store } from "pullstate";

const defGlobalStore = {
  loading: false,
  forms: [],
  settingCascadeURL: [],
};

const GlobalStore = new Store({
  ...defGlobalStore,
});

export default GlobalStore;
