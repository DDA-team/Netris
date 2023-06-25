<template>
    <nav class="navbar fixed-top navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">DDA</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
                aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Переключатель навигации">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                </div>
            </div>
            <div class="d-flex mr-5">
                <a href="/" class="btn btn-primary mr-auto">На главную</a>
            </div>
        </div>

    </nav>
    <div class="container mt-5">
        <!-- <div class="row mt-5">
            <div class="col-6 mt-5">
                <h4>Оригинал:</h4>
                <video controls class="width-video">
                    <source :src="'http://195.239.123.50:9000/items/inputvideo/' + id" type="video/mp4">
                </video>
            </div>
            <div class="col-6 mt-5">
                <h4>Обработанное видео:</h4>
                <video controls class="width-video" preload="metadata">
                </video>
            </div>
        </div> -->
        <div class="row mt-5">
            <div class="col-12 mt-5 mb-4">
                <ul class="nav nav-pills">
                    <li class="nav-item">
                        <a class="nav-link" :class="{ active: this.state == 'info' }" aria-current="page"
                            @click="setState('info')" href=" #">Информация</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" :class="{ active: this.state == 'events' }" href="#"
                            @click="setState('events')">События</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" :class="{ active: this.state == 'events_waste' }" href="#"
                            @click="setState('events_waste')">Журнал простоя</a>
                    </li>
                </ul>
            </div>
        </div>
        <table id="example" class="table table-striped " style="width:100%" v-if="this.state == 'events'">
            <thead>
                <tr>
                    <th>ID События</th>
                    <th>ID Объекта</th>
                    <th>Класс</th>
                    <th>Время начала</th>
                    <th>Время конца</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(event, key) in this.events" :key="key">
                    <td>{{ key }}</td>
                    <td>{{ event.id }}</td>
                    <td>{{ event.class }}</td>
                    <td>{{ event.start_time }}</td>
                    <td>{{ event.end_time }}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th>ID События</th>
                    <th>ID Объекта</th>
                    <th>Класс</th>
                    <th>Время начала</th>
                    <th>Время конца</th>
                </tr>
            </tfoot>
        </table>
        <table id="example" class="table table-striped " style="width:100%" v-if="this.state == 'events_waste'">
            <thead>
                <tr>
                    <th>ID Объекта</th>
                    <th>Время простоя</th>
                    <th>Время активности</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(event, key) in this.events_waste" :key="key">
                    <td>{{ key }}</td>
                    <td>{{ event.active }}</td>
                    <td>{{ event.passive }}</td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th>ID Объекта</th>
                    <th>Время простоя</th>
                    <th>Время активности</th>
                </tr>
            </tfoot>
        </table>
        <div v-if="this.state == 'info'">
            <div class="row">
                <div class="col-6">
                    <img :src="this.host + 'items/preview/output/' + this.item.id" class="d-block w-100"
                        alt="src\assets\0JtChN7jaJs.jpg">
                </div>
                <div class="col-3">
                    <p class="info">Имя видео: {{ this.item.title }}<br>Длительность: {{ this.toDateTime }}<br>Количество
                        событий: {{ Object.keys(this.events).length }}<br>Количество
                        объектов: {{ Object.keys(this.events_waste).length }}</p>
                    <a :href="this.host + 'items/download/output/' + this.item.id" class="btn btn-primary mt-2 w-100"
                        download="true">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-download" viewBox="0 0 16 16">
                            <path
                                d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z" />
                            <path
                                d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z" />
                        </svg> Скачать обработанное видео</a>
                    <a :href="this.host + 'items/download/events/' + this.item.id" class="btn btn-primary mt-2 w-100"
                        download><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-download" viewBox="0 0 16 16">
                            <path
                                d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z" />
                            <path
                                d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z" />
                        </svg> Скачать json событий</a>
                    <a :href="this.host + 'items/download/downtime/' + this.item.id" class="btn btn-primary mt-2 w-100"
                        download><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-download" viewBox="0 0 16 16">
                            <path
                                d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z" />
                            <path
                                d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z" />
                        </svg> Скачать json журнала простоя</a>
                    <!-- <p>Количество событий: {{ this.events.lenght }}</p> -->
                </div>
            </div>

        </div>
    </div>
</template>

<style>
.width-video {
    max-width: 100%;
    min-width: 100%;
    min-height: 310px;
}

.info {
    text-align: left;
    font-size: large;
}
</style>

<script>
import axios from "axios"
// import $ from 'jquery'
// import DataTable from 'datatables.net';

export default {
    name: 'HomeView',
    components: {
    },
    data() {
        return {
            item: { 'title': null },
            state: 'info',
            host: "http://195.239.123.50:9000/",
            events: {},
            events_waste: {}
        }
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
        getEvents() {
            axios.get(this.host + 'items/events/' + this.id).then((resp) => {
                console.log(this);
                this.events = resp.data
            })
                .catch(function (er) {
                    console.log(er);
                });
        },
        getEventsWaste() {
            axios.get(this.host + 'items/downtime/' + this.id).then((resp) => {
                console.log(this);
                this.events_waste = resp.data
            })
                .catch(function (er) {
                    console.log(er);
                });
        },
        // createDataTable() {
        //     var dt = new DataTable();
        //     return dt
        // },
        setState(state) {
            this.state = state;
        }
    },
    created() {
        this.getItem()
        this.getEvents()
        this.getEventsWaste()
    },
    mounted() {
        // $(document).ready(function () {
        //     $('#example').DataTable();
        // });
    },
    computed: {
        id() {
            return this.$route.params.id;
        },
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
    },
}
</script>