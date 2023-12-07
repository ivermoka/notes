<script setup lang="ts">

const props = defineProps({
  data: Array,
  titleValue: String,
  noteValue: String,
})
const title = props.data[1];
const note = props.data[2];
const updateValues  = {
  titleValue: title,
  noteValue: note,
}
</script>
<template>
  <div class="text-black px-2 bg-gray-500">
    <div class="flex justify-between ">
      <button @click="$emit('push', updateValues)" class="text-xl font-bold">Push</button>
      <button class="text-xl font-bold">X</button>
    </div>
    <div class="h-[40vh] w-full rounded-sm pb-2" @change="$emit('updateValues', {title: title, note: note})">
      <textarea :value="title" class="w-full resize-none" placeholder="Note name">{{title}}</textarea>
      <textarea :value="note" class="w-full h-5/6 p-1 resize-none" placeholder="Your note">{{note}}</textarea>
    </div>

  </div>
</template>
