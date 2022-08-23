package com.myapps.seriesmanager.controller;

import com.myapps.seriesmanager.service.SeriesService;
import com.myapps.seriesmanager.service.SubscribersNewSeriesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.io.IOException;
import java.util.ArrayList;

@Controller
@RequestMapping("/rest")
public class SeriesController {

    private final SeriesService seriesService;
    private final SubscribersNewSeriesService subscribersNewSeriesService;

    @Autowired
    public SeriesController(SeriesService seriesService, SubscribersNewSeriesService subscribersNewSeriesService) {
        this.seriesService = seriesService;
        this.subscribersNewSeriesService = subscribersNewSeriesService;
    }

    @GetMapping("/updateSeries")
    public ResponseEntity updateSeries() {
        try {
            seriesService.updateSeries();
            return ResponseEntity.ok(200);
        } catch (IOException e) {
            e.printStackTrace();
            return ResponseEntity.badRequest().body(400);
        }
    }

    @GetMapping("/subAll")
    public ResponseEntity subAll(@RequestParam Long id, @RequestParam boolean vk) {
        seriesService.testSubAll(id, vk);
        return ResponseEntity.ok(200);
    }

    @GetMapping("/getSeries")
    public ResponseEntity getSeries(@RequestParam String names) {
        if (names != null) {
            return ResponseEntity.ok(seriesService.getSeries(names.split(";")));
        } else {
            return ResponseEntity.badRequest().body(new ArrayList<>());
        }
    }

    @GetMapping("/getAllSeries")
    public ResponseEntity getAllSeries() {
        return ResponseEntity.ok(seriesService.getAll());
    }

    @GetMapping("/addNewSeries")
    public ResponseEntity addNewSeries(@RequestParam String name, @RequestParam(required = false) String additional) {
        if (name != null && additional != null) {
            if (seriesService.addNewSeries(name, additional)) {
                return ResponseEntity.ok(200);
            }
        }
        return ResponseEntity.badRequest().body(400);
    }

    @GetMapping("/getSeriesWithSameName")
    public ResponseEntity getSeriesWithSameName(@RequestParam String name) {
        if (name != null) {
            return ResponseEntity.ok(seriesService.getSeriesWithSameName(name));
        } else {
            return ResponseEntity.badRequest().body(400);
        }
    }

    @GetMapping("/getSubscribedSeries")
    public ResponseEntity getSubscribedSeries(@RequestParam Long id, @RequestParam boolean vk) {
        if (id != null) {
            return ResponseEntity.ok(seriesService.getSubscribedSeries(id, vk));
        } else {
            return ResponseEntity.badRequest().body(400);
        }
    }

    @GetMapping("/subscribe")
    public ResponseEntity subscribe(@RequestParam Long id, @RequestParam String name, @RequestParam int num, @RequestParam boolean vk) {
        if (id != null && name != null) {
            String response = seriesService.subscribe(id, name, num, vk);
            return ResponseEntity.ok(response);
        }
        return ResponseEntity.badRequest().body(400);
    }

    @GetMapping("/unsubscribe")
    public ResponseEntity unsubscribe(@RequestParam Long id, @RequestParam String name, @RequestParam int num, @RequestParam boolean vk) {
        if (id != null && name != null) {
            String response = seriesService.unsubscribe(id, name, num, vk);
            return ResponseEntity.ok(response);
        }
        return ResponseEntity.badRequest().body(400);
    }

    @GetMapping("/subscribeNewSeries")
    public ResponseEntity subscribeNewSeries(@RequestParam Long id, @RequestParam boolean vk) {
        if (id != null) {
            String response = subscribersNewSeriesService.subscribeNewSeries(id, vk);
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.badRequest().body(400);
        }
    }

    @GetMapping("/unsubscribeNewSeries")
    public ResponseEntity unsubscribeNewSeries(@RequestParam Long id, @RequestParam boolean vk) {
        if (id != null) {
            String response = subscribersNewSeriesService.unsubscribeNewSeries(id, vk);
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.badRequest().body(400);
        }
    }

    @GetMapping("/getSubscribersNewSeries")
    public ResponseEntity getSubscribersNewSeries(@RequestParam boolean vk) {
        return ResponseEntity.ok(subscribersNewSeriesService.getSubscribers(vk));
    }

    @GetMapping("/getSubscribers")
    public ResponseEntity getSubscribers(@RequestParam boolean vk) {
        return ResponseEntity.ok(seriesService.getSubscribers(vk));
    }
}
