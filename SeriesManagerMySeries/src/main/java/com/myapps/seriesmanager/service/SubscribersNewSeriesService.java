package com.myapps.seriesmanager.service;

import com.myapps.seriesmanager.entity.SubscribersNewSeriesEntity;
import com.myapps.seriesmanager.repository.SubscribersNewSeriesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class SubscribersNewSeriesService {

    private final SubscribersNewSeriesRepository subscribersNewSeriesRepository;

    @Autowired
    public SubscribersNewSeriesService(SubscribersNewSeriesRepository subscribersNewSeriesRepository) {
        this.subscribersNewSeriesRepository = subscribersNewSeriesRepository;
    }

    public String subscribeNewSeries(Long id, boolean vk) {
        if (subscribersNewSeriesRepository.findAll().isEmpty()) {
            subscribersNewSeriesRepository.save(new SubscribersNewSeriesEntity());
        }
        SubscribersNewSeriesEntity subscribersNewSeriesEntity = subscribersNewSeriesRepository.findAll().get(0);
        if (vk) {
            List<Long> result = subscribersNewSeriesEntity.getVKSubs();
            if (!result.contains(id)) {
                result.add(id);
                subscribersNewSeriesEntity.setVKSubs(result);
            } else {
                return "Already subscribed";
            }
        } else {
            List<Long> result = subscribersNewSeriesEntity.getTGSubs();
            if (!result.contains(id)) {
                result.add(id);
                subscribersNewSeriesEntity.setTGSubs(result);
            } else {
                return "Already subscribed";
            }
        }
        subscribersNewSeriesRepository.save(subscribersNewSeriesEntity);
        return "Subscribed";
    }

    public String unsubscribeNewSeries(Long id, boolean vk) {
        if (subscribersNewSeriesRepository.findAll().isEmpty()) {
            subscribersNewSeriesRepository.save(new SubscribersNewSeriesEntity());
        }
        SubscribersNewSeriesEntity subscribersNewSeriesEntity = subscribersNewSeriesRepository.findAll().get(0);
        if (vk) {
            List<Long> result = subscribersNewSeriesEntity.getVKSubs();
            if (result.contains(id)) {
                result.remove(id);
                subscribersNewSeriesEntity.setVKSubs(result);
            } else {
                return "Already unsubscribed";
            }
        } else {
            List<Long> result = subscribersNewSeriesEntity.getTGSubs();
            if (result.contains(id)) {
                result.remove(id);
                subscribersNewSeriesEntity.setTGSubs(result);
            } else {
                return "Already unsubscribed";
            }
        }
        subscribersNewSeriesRepository.save(subscribersNewSeriesEntity);
        return "Unsubscribed";
    }

    public List<Long> getSubscribers(boolean vk) {

        List<Long> result = new ArrayList<>();

        if (!subscribersNewSeriesRepository.findAll().isEmpty()) {
            SubscribersNewSeriesEntity subscribersNewSeriesEntity = subscribersNewSeriesRepository.findAll().get(0);
            if (vk) {
                result.addAll(subscribersNewSeriesEntity.getVKSubs());
            } else {
                result.addAll(subscribersNewSeriesEntity.getTGSubs());
            }
        }
        return result;
    }

}
