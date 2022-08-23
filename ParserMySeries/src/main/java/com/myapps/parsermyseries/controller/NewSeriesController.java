package com.myapps.parsermyseries.controller;

import com.myapps.parsermyseries.service.NewSeriesService;
import com.myapps.parsermyseries.service.NoveltySeriesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
@RequestMapping("/rest")
public class NewSeriesController {

    private final NewSeriesService newSeriesService;
    private final NoveltySeriesService noveltySeriesService;

    @Autowired
    public NewSeriesController(NewSeriesService newSeriesService, NoveltySeriesService noveltySeriesService) {
        this.newSeriesService = newSeriesService;
        this.noveltySeriesService = noveltySeriesService;
    }

    @GetMapping("/remove")
    public ResponseEntity deprecateOldData(@RequestParam boolean vk) {
        newSeriesService.deprecateData(vk);;
        return ResponseEntity.ok(200);
    }

    @GetMapping("/newSeries")
    public ResponseEntity getNewSeries(@RequestParam boolean vk) {
        return ResponseEntity.ok(newSeriesService.getAllSeries(vk));
    }

    @GetMapping("/removeNovelties")
    public ResponseEntity deprecateOldNovelties(@RequestParam boolean vk) {
        noveltySeriesService.deprecateNovelties(vk);
        return ResponseEntity.ok(200);
    }

    @GetMapping("/novelties")
    public ResponseEntity getNovelties(@RequestParam boolean vk) {
        return ResponseEntity.ok(noveltySeriesService.getAllNovelties(vk));
    }
}
