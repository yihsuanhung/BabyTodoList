<template>
  <div>
    <button @click="taskdoneT1()">Done</button>
    <!-- <button @click="test()">BUT</button> -->
  </div>
</template>

<script>
import sendReq from "@/plugins/sendReq";
import process from "@/plugins/preprocess.js";
import classifier from "@/plugins/classifier.js";
import { API } from "@/constants/config";
import { EventBus } from "@/plugins/bus.js";
export default {
  name: "Done",
  props: ["inPage", "inLimit"],
  data() {
    return {
      apiURL: API.Host + ":" + API.Port,
      selection: []
    };
  },
  methods: {
    async taskdone() {
      if (this.selection.length !== 0) {
        for (let i = 0; i < this.selection.length; i++) {
          let taskId = this.selection[i];
          let config = {
            baseURL: this.apiURL,
            url: "/done/" + Number(taskId),
            method: "put",
            params: {
              page: this.inPage,
              limit: this.inLimit
            }
          };
          let result = await sendReq(config);
          let data = result["data"];
          this.$emit("outData", data);
          this.outData = data;
        }
        EventBus.$emit("TasksSelectionBus", []);
        this.$forceUpdate();
      }
    },
    async taskdoneT1() {
      // console.log(this.$store.state.vxSelection)
      // console.log(this.$store.state.vxSelection.length)
      if (this.$store.state.vxSelection.length !== 0) {
        for (let i = 0; i < this.$store.state.vxSelection.length; i++) {
          let taskId = this.$store.state.vxSelection[i];
          let config = {
            baseURL: this.apiURL,
            url: "/done/" + Number(taskId),
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
        }
        // EventBus.$emit("TasksSelectionBus", []);
        this.$store.dispatch("selectionAction", []);
        this.$forceUpdate();
      }
    },
    test() {
      // console.log("hi")
      console.log(this.$store.state.vxSelection);
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
