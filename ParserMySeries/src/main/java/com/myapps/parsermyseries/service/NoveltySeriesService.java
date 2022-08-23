package com.myapps.parsermyseries.service;

import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.HtmlAnchor;
import com.gargoylesoftware.htmlunit.html.HtmlElement;
import com.gargoylesoftware.htmlunit.html.HtmlImage;
import com.gargoylesoftware.htmlunit.html.HtmlPage;
import com.myapps.parsermyseries.entity.NewSeriesEntity;
import com.myapps.parsermyseries.entity.NoveltySeriesEntity;
import com.myapps.parsermyseries.repository.NoveltySeriesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.List;
import java.util.concurrent.TimeUnit;

@Service
public class NoveltySeriesService {

    private final String LINK = "http://myseria.pro/newest/";

    private final NoveltySeriesRepository noveltySeriesRepository;

    @Autowired
    public NoveltySeriesService(NoveltySeriesRepository noveltySeriesRepository) {
        this.noveltySeriesRepository = noveltySeriesRepository;
    }

    @Scheduled(fixedDelay = 3, timeUnit = TimeUnit.MINUTES)
    public void parseAndSaveNoveltySeries() throws IOException {

        final WebClient webClient = new WebClient();

        webClient.getOptions().setJavaScriptEnabled(false);
        webClient.getOptions().setCssEnabled(false);

        HtmlPage page = webClient.getPage(LINK);

        HtmlElement newsMonth = page.getFirstByXPath(".//html//body//div[@class='wrapper']//main[@class='main']//div[@class='l-main']//div[@class='row']//div[@class='small-12 columns']//div[@class='l-main-content white']//div[@class='news-month']");
        HtmlElement novelties = newsMonth.getFirstByXPath(".//div[@class='block-new-serials box-popover-5 episode-group-wrapper']//div[@class='episode-group']//div[@class='block-content block-content_0']//div[@class='block-list']");
        List<HtmlElement> noveltyList = (List<HtmlElement>) novelties.getByXPath(".//div[@class='owl-item']");
        for (HtmlElement novelty : noveltyList) {
            HtmlElement element = novelty.getFirstByXPath(".//div[@class='item']//div[@class='new-serials-item']");
            String name = ((HtmlElement) element.getFirstByXPath(".//div[@class='field-title']//a")).getTextContent();
            String url = ((HtmlAnchor) element.getFirstByXPath(".//div[@class='field-title']//a")).getHrefAttribute();
            String pictureUrl = "http://myseria.pro" + ((HtmlImage) element.getFirstByXPath(".//div[@class='new-serials-poster']//a[@class='field-poster']//img")).getSrcAttribute();

            if (noveltySeriesRepository.findByName(name) == null) {
                noveltySeriesRepository.save(new NoveltySeriesEntity(name, url, pictureUrl));
            }
        }

    }

    public void deprecateNovelties(boolean vk) {
        noveltySeriesRepository.findAll().forEach((p) -> {
            if (vk) {
                p.setVKDeprecated(true);
            } else {
                p.setTGDeprecated(true);
            }
            noveltySeriesRepository.save(p);
        });
    }

    public List<NoveltySeriesEntity> getAllNovelties(boolean vk) {
        if (vk) {
            return noveltySeriesRepository.findAllByVKDeprecated(false);
        }
        return noveltySeriesRepository.findAllByTGDeprecated(false);
    }
}
