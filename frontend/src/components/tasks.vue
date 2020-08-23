<template>
  <div>
    <h3>Tasks Todo</h3>
    <ul class="undoTasks">
      <li v-for="(item, index) in inData.undo" :key="index">
        <input
          type="checkbox"
          :value="item['id']"
          v-model="vxs"
          @change="emitSelection()"
        />
        {{ item["id"] }},
        {{ item["content"] }}
        <button
          @click="EditStatSwitch(item['id'], 'undo')"
          v-if="!item['editStatus']"
        >
          Edit
        </button>
        <input
          type="text"
          v-if="item['editStatus']"
          v-model="item['editContent']"
          @keyup.enter="Edit(item['id'], item['editContent'])"
        />
        <button
          @click="Edit(item['id'], item['editContent'])"
          v-if="item['editStatus']"
        >
          Update
        </button>
        <button
          @click="EditStatSwitch(item['id'], 'undo')"
          v-if="item['editStatus']"
        >
          Cancel
        </button>
      </li>
    </ul>

    <h3>Tasks Done</h3>
    <ul class="doneTasks">
      <li v-for="(item, index) in inData.done" :key="index">
        <input
          type="checkbox"
          :value="item['id']"
          v-model="vxs"
          @change="emitSelection()"
        />
        {{ item["id"] }},
        {{ item["content"] }}
        <button
          @click="EditStatSwitch(item['id'], 'done')"
          v-if="!item['editStatus']"
        >
          Edit
        </button>
        <input
          type="text"
          v-if="item['editStatus']"
          v-model="item['editContent']"
          @keyup.enter="Edit(item['id'], item['editContent'])"
        />
        <button
          @click="Edit(item['id'], item['editContent'])"
          v-if="item['editStatus']"
        >
          Update
        </button>
        <button
          @click="EditStatSwitch(item['id'], 'done')"
          v-if="item['editStatus']"
        >
          Cancel
        </button>
      </li>
    </ul>
    <!-- <div>selected ids: {{ selectedIds }}</div> -->
    <div>selection: {{ vxs }}</div>
    <!-- <div>vuex fetchedData: {{ this.$store.state.vxFetchedData }}</div> -->
    <div><button @click="checkStore()">Check State</button></div>
    <br />
  </div>
</template>

<script>
import sendReq from "@/plugins/sendReq";
// import classify from "@/plugins/classifier";
// import process from "@/plugins/sendReq";
import { API } from "@/constants/config";
import { EventBus } from "@/plugins/bus.js";
// import { mapState } from "vuex";
export default {
  name: "Tasks",
  props: {
    inData: Object,
    inPage: Number,
    inLimit: Number
  },
  data() {
    return {
      apiURL: API.Host + ":" + API.Port,
      selection: []
      // vxs: []
    };
  },
  created() {},
  mounted() {
    EventBus.$on("TasksSelectionBus", arr => {
      this.selection = arr;
    });
  },
  computed: {
    vxs: {
      get: function() {
        return this.$store.state.vxSelection;
      },
      set: function(arr) {
        // console.log('')
        // console.log('setter', arr)
        // this.vxs = this.$store.state.vxSelection;
        this.$store.dispatch("selectionAction", arr);
      }
    }
    // ...mapState(["vxSelection"])
  },
  methods: {
    fakeLogInTasks() {
      console.log(this.$store.state.fakeInfo.isLogin);
      this.$store.dispatch("fakeCheckLoginStatus", "randomArg");
      console.log(this.$store.state.fakeInfo.isLogin);
    },
    emitSelection() {
      // this.$emit("TaskOutSelect", this.selection);

      // Eventbus
      // EventBus.$emit("TasksSelectionBus", this.selection);

      // Vuex
      this.$store.dispatch("selectionAction", this.vxs);

      // this.selection = [];
    },
    checkStore() {
      console.log(this.$store.state.vxSelection);
    },
    preprocess(objArr) {
      // Add two field, 'editStatus' and 'editContent', to each object
      let processed = [];
      for (let i = 0; i < objArr.length; i++) {
        let obj = objArr[i];
        obj["editStatus"] = false;
        obj["editContent"] = "";
        processed.push(obj);
      }
      return processed;
    },
    EditStatSwitch(task_id, mode) {
      if (mode === "undo") {
        for (let i = 0; i < this.inData.undo.length; i++) {
          if (this.inData.undo[i]["id"] === task_id) {
            this.inData.undo[i]["editStatus"] = !this.inData.undo[i][
              "editStatus"
            ];
          }
        }
      } else if (mode === "done") {
        for (let i = 0; i < this.inData.done.length; i++) {
          if (this.inData.done[i]["id"] === task_id) {
            this.inData.done[i]["editStatus"] = !this.inData.done[i][
              "editStatus"
            ];
          }
        }
      }
    },
    async Edit(task_id, editedTask) {
      if (editedTask !== "") {
        let config = {
          baseURL: this.apiURL,
          url: "/edit/" + Number(task_id),
          method: "put",
          params: {
            page: this.inPage,
            limit: this.inLimit
          },
          data: JSON.stringify({ content: editedTask })
        };
        let result = await sendReq(config);
        let data = result["data"];
        // data = classify(data);
        // data = data.undo;
        // data = this.preprocess(data);
        this.$emit("outData", data);
        // this.fetchedData.undo=[]
        // this.fetchedData.done=[]
        // classify(data, this.fetchedData.undo, this.fetchedData.done)
      }
    }
  }
};
</script>
<style lang="stylus">
.undoTasks {
    text-align:left;
    display: inline-block;
    list-style-type: none;
}
.doneTasks {
    color: #BDBDBD;
    text-align:left;
    display: inline-block;
    list-style-type: none;
}
.doneEditBut{
    color: #757575;
}
</style>
