using fa_eventhub_to_sonia.models.common;
using Newtonsoft.Json;
using System;

namespace fa_eventhub_to_sonia.models.events {
    public class CourseOccurrence {
        [JsonProperty("occurrenceId")]
        public string OccurrenceId { get; set; }

        [JsonProperty("courseId")]
        public string CourseId { get; set; }

        [JsonProperty("code")]
        public string Code { get; set; }

        [JsonProperty("semester")]
        public Semester Semester { get; set; }

        [JsonProperty("status")]
        public string Status { get; set; }

        [JsonProperty("site")]
        public GenericCodeDesc Site { get; set; }

        [JsonProperty("contributors")]
        public Contributor[] Contributors { get; set; }

        [JsonProperty("orgUnitDelivering")]
        public string OrgUnitDelivering { get; set; }

        [JsonProperty("startDate")]
        [JsonConverter(typeof(DateFormatter), "yyyy-MM-dd")]
        public DateTime StartDate { get; set; }

        [JsonProperty("endDate")]
        [JsonConverter(typeof(DateFormatter), "yyyy-MM-dd")]
        public DateTime EndDate { get; set; }

        [JsonProperty("maxEnrolments")]
        public int MaxEnrolments { get; set; }

        [JsonProperty("minEnrolments")]
        public int MinEnrolments { get; set; }

        [JsonProperty("deliveryMode")]
        public string DeliveryMode { get; set; }
        
        [JsonProperty("courseFactor")]
        public int CourseFactor { get; set; }
        
        [JsonProperty("costCategory")]
        public GenericCodeDesc CostCategory { get; set; }
        
        [JsonProperty("fundingClassification")]
        public string FundingClassification { get; set; }

        [JsonProperty("courseCreatedDate")]
        [JsonConverter(typeof(DateFormatter), "yyyy-MM-ddThh:MM:ss.ffffffZ")]
        public DateTime CourseCreatedDate { get; set; }

        [JsonProperty("funds")]
        public FeeBands Funds { get; set; }

        [JsonProperty("firstTimeOffered")]
        public bool FirstTimeOffered { get; set; }
        
        [JsonProperty("allowsCrossYearEnrolment")]
        public bool AllowsCrossYearEnrolment { get; set; }
    }

    public class Semester {
        [JsonProperty("code")]
        public string Code { get; set; }

        [JsonProperty("indicator")]
        public string Indicator { get; set; }
    }

    public class Contributor {
        [JsonProperty("contributor")]
        public string ContributorName { get; set; }

        [JsonProperty("role")]
        public string Role { get; set; }
    }
}