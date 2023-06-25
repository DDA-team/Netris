<template>
    <div class="card" style="width: 25rem;">
        <div :class="{ 'processing-mask': !this.status }">
            <div class="position-relative">
                <div v-if="!this.status" class="spinner-border spinner-process" style="width: 3rem; height: 3rem;"
                    role="status">
                    <span class="visually-hidden">Загрузка...</span>
                </div>
                <img :src="this.host + 'items/preview/' + this.id" class="card-img-top custom-card" alt="...">

            </div>

        </div>
        <div class="card-body">
            <h5 class="card-title">{{ this.item.title }}</h5>
            <p>Длительность видео: {{ this.toDateTime }}<br />Статус: {{ this.stateComputed }}</p>
        </div>

        <div class="card-body d-flex justify-content-between">
            <a :href="'/item/' + this.id" class="btn btn-primary mr-auto"
                :class="{ 'disabled': !this.status }">Подробнее</a>
            <button class="btn btn-danger ml-auto" @click="removeItem()">Удалить</button>


        </div>
    </div>
</template>

<style>
.custom-card {
    min-height: 250px;
    max-height: 250px;
}

.processing-mask {
    background-color: aliceblue;
    opacity: 0.5;
    width: 25rem;
    height: auto;

}

.spinner-process {
    position: absolute;
    width: 3rem;
    top: 40%;
    left: 44%;
    right: 40%;
    z-index: 100;
}

.remove-button {
    position: absolute;
    color: aliceblue;
    top: 2.5%;
    right: 2.5%;
    z-index: 100;
    opacity: 1;
    transition-property: color;
    transition-duration: .2s;
}

.remove-button:hover {
    position: absolute;
    color: red;
    top: 2.5%;
    right: 2.5%;
    z-index: 100;
    opacity: 1;
}
</style>

<script>
import axios from "axios"

export default {
    name: 'ProcessingTemplate',
    data() {
        return {
            host: "http://195.239.123.50:9000/",
            item: "",
            status: null
        }
    },
    props: {
        id: String
    },
    methods: {
        getItem() {
            axios.get(this.host + 'items/' + this.id).then((resp) => {
                console.log(this);
                this.item = resp.data
            })
                .catch(function (er) {
                    console.log(er);
                });
        },
        getStatus() {
            axios.get(this.host + 'items/status/' + this.id).then((resp) => {
                console.log(this);
                this.status = resp.data
            })
                .catch(function (er) {
                    console.log(er);
                });
        },
        removeItem() {
            axios.post(this.host + 'items/remove/' + this.id).then(() => {
                console.log(this);
                this.$emit('remove-event')
            })
                .catch(function (er) {
                    console.log(er);
                });
        }
    },
    created() {
        this.getItem()
        this.getStatus()
        setInterval(() => {
            this.getStatus()
        }, 5000);
    },
    computed: {
        toDateTime: function () {
            var timestamp = this.item.duration;
            var hours = Math.floor(timestamp / 60 / 60);
            var minutes = Math.floor(timestamp / 60) - (hours * 60);
            var seconds = timestamp % 60;
            var formatted = [
                hours.toString().padStart(2, '0'),
                minutes.toString().padStart(2, '0'),
                seconds.toString().padStart(2, '0')
            ].join(':')
            return formatted
        },
        stateComputed: function () {
            if (this.status) {
                return "Обработано"
            }
            else {
                return "Не обработано"
            }
        }
    }
}
</script>