<template>
  <button @click="test()">TEST</button>
</template>

<script>
import { EventBus } from "@/plugins/bus.js";
export default {
  name: "Test",
  data() {
    return {
      num: 101
    };
  },
  methods: {
    test() {
      console.log("message from fake.vue");
      EventBus.$emit("testbus", this.num);
    }
  }
};
</script>
