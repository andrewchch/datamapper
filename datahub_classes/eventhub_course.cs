using fa_eventhub_to_sonia.models.common;
using Newtonsoft.Json;
using System;

namespace fa_eventhub_to_sonia.models.events {
    public class Course {
        [JsonProperty("courseId")]
        public string CourseId { get; set; }

        [JsonProperty("qualificationId")]
        public string QualificationId { get; set; }

        [JsonProperty("code")]
        public string Code { get; set; }

        [JsonProperty("title")]
        public string Title { get; set; }

        [JsonProperty("shortTitle")]
        public string ShortTitle { get; set; }

        [JsonProperty("linkedCodes")]
        public GenericCodeDesc[] LinkedCodes { get; set; }

        [JsonProperty("subject")]
        public string Subject { get; set; }

        [JsonProperty("status")]
        public string Status { get; set; }

        [JsonProperty("faculties")]
        public CourseFaculty[] Faculties { get; set; }

        [JsonProperty("isWIL")]
        public bool IsWIL { get; set; }

        [JsonProperty("isThesis")]
        public bool IsThesis { get; set; }

        [JsonProperty("level")]
        public int Level { get; set; }

        [JsonProperty("creditValue")]
        public int CreditValue { get; set; }

        [JsonProperty("eftsWeight")]
        public float EFTSWeight { get; set; }

        [JsonProperty("feeBands")]
        public FeeBands FeeBands { get; set; }

        [JsonProperty("nzSched")]
        public string NZSched { get; set; }

        [JsonProperty("fundingCode")]
        public string FundingCode { get; set; }

        [JsonProperty("maxEnrolments")]
        public int MaxEnrolments { get; set; }

        [JsonProperty("minEnrolments")]
        public int MinEnrolments { get; set; }

        [JsonProperty("createdDate")]
        [JsonConverter(typeof(DateFormatter), "yyyy-MM-dd")]
        public DateTime CreatedDate { get; set; }

        [JsonProperty("retirementDate")]
        [JsonConverter(typeof(DateFormatter), "yyyy-MM-dd")]
        public DateTime RetirementDate { get; set; }

        [JsonProperty("deliveryMode")]
        public string DeliveryMode { get; set; }

        [JsonProperty("costCategory")]
        public GenericCodeDesc CostCategory { get; set; }
    }

    public class CourseFaculty {
        [JsonProperty("code")]
        public string Code { get; set; }

        [JsonProperty("faculty")]
        public string Faculty { get; set; }

        [JsonProperty("departments")]
        public GenericCodeDesc[] Departments { get; set; }
    }
}