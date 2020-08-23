<template>
  <div>
    <button @click="taskundoT1()">Undo</button>
  </div>
</template>

<script>
import sendReq from "@/plugins/sendReq";
import process from "@/plugins/preprocess.js";
import classifier from "@/plugins/classifier.js";
import { API } from "@/constants/config";
import { EventBus } from "@/plugins/bus.js";
export default {
  name: "Undo",
  props: ["inPage", "inLimit"],
  data() {
    return {
      apiURL: API.Host + ":" + API.Port,
      selection: []
    };
  },
  methods: {
    async taskundo() {
      if (this.selection.length !== 0) {
        for (let i = 0; i < this.selection.length; i++) {
          let taskId = this.selection[i];
          let config = {
            baseURL: this.apiURL,
            url: "/undo/" + Number(taskId),
            method: "put",
            params: {
              page: this.inPage,
              limit: this.inLimit
            }
          };
          let result = await sendReq(config);
          let data = result["data"];
          this.$emit("outData", data);
        }
        this.$forceUpdate();
      }
      EventBus.$emit("TasksSelectionBus", []);
    },
    async taskundoT1() {
      if (this.$store.state.vxSelection.length !== 0) {
        for (let i = 0; i < this.$store.state.vxSelection.length; i++) {
          let taskId = this.$store.state.vxSelection[i];
          let config = {
            baseURL: this.apiURL,
            url: "/undo/" + Number(taskId),
            method: "put",
            params: {
              page: this.inPage,
              limit: this.inLimit
            }
          };
          let result = await sendReq(config);
          let data = result["data"];
          data = process(data);
          data = classifier(data);
          this.$store.dispatch("fetchedDataAction", data);
          // console.log("Set undo!");
        }
        this.$store.dispatch("selectionAction", []);
        this.$forceUpdate();
      }
    }
  },
  created() {
    EventBus.$on("TasksSelectionBus", arr => {
      this.selection = arr;
    });
  },
  beforeDestroy: function() {
    EventBus.$off();
  }
};
</script>
